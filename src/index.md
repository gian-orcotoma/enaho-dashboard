---
toc: false
sql:
  problemas: data/grafico1_dataloader.json
  corrupcion_1: data/grafico2_dataloader.json
  corrupcion: data/grafico3_dataloader.json
  gestion_gobierno: data/grafico5_dataloader.json
  entidades: data/grafico4_dataloader.json
  democraciaElecciones: data/grafico6_dataloader.json
---
# Dashboard de Percepcion Ciudadana

<div class="grid grid-cols-4">
  <div class="card" style="color: inherit;">
    <h2>Principal problema del país</h2>
    <span class="big">Corrupción</span>
  </div>
</div>


## 1. Los principales problemas del pais

```sql id=problemasFiltrado
SELECT * FROM(
  SELECT * FROM (
    SELECT
      VALOR
      ,AÑO
      ,FECHA
      ,PREGUNTA_NOM
      ,PREGUNTA_COD
      --,FACTOR07
      ,SUM(VALOR) OVER (
        PARTITION BY PREGUNTA_COD
        ORDER BY FECHA
        ROWS BETWEEN ${movil_meses-1} PRECEDING AND CURRENT ROW
      ) / SUM(FACTOR07) OVER (
        PARTITION BY PREGUNTA_COD
        ORDER BY FECHA
        ROWS BETWEEN ${movil_meses-1} PRECEDING AND CURRENT ROW
      ) * 100
       AS PROMEDIO_MOVIL
    FROM problemas
  )
  WHERE
    AÑO >= ${year_inicio}
    AND AÑO <= ${year_fin}
) AS Prob INNER JOIN (
  -- Seleccionar TOP del ultimo semestre
  SELECT
    PREGUNTA_COD
  FROM (
    SELECT
      VALOR
      ,AÑO
      ,FECHA
      ,PREGUNTA_NOM
      ,PREGUNTA_COD
      ,SUM(VALOR) OVER (
        PARTITION BY PREGUNTA_COD
        ORDER BY FECHA
        ROWS BETWEEN ${movil_meses-1} PRECEDING AND CURRENT ROW
      ) / SUM(FACTOR07) OVER (
        PARTITION BY PREGUNTA_COD
        ORDER BY FECHA
        ROWS BETWEEN ${movil_meses-1} PRECEDING AND CURRENT ROW
      ) * 100
       AS PROMEDIO_MOVIL
    FROM problemas
  )
  WHERE
    FECHA == CONCAT(CAST(${year_fin} AS INT), '-12')
  ORDER BY PROMEDIO_MOVIL DESC
  LIMIT 7
) As Toplist ON Prob.PREGUNTA_COD = Toplist.PREGUNTA_COD
```


```js
// Inputs
let [{max_year}] = await sql`select max(AÑO) as max_year from problemas`
max_year = 2023
const [{min_year}] = await sql`select min(AÑO) as min_year from problemas`


const year_inicio_input = Inputs.range([min_year, max_year], {
  step: 1,
  label: "Desde",
  value: max_year-2 }
)
const year_inicio = Generators.input(year_inicio_input);

const year_fin_input = Inputs.range([min_year, max_year], {
  step: 1,
  label: "Hasta",
  value: max_year,
  validate: (val)=>{return val>=year_inicio? true : false}}
)
const year_fin = Generators.input(year_fin_input);

const movil_opciones = new Map([["Año", 12], ["Semestre", 6], ["Trimestre", 3], ["Mes", 1]])
const movil_nombres = new Map([[12, "Año"], [6, "Semestre"], [3, "Trimestre"], [1, "Mes"]])
const movil_meses_input = Inputs.select(
  movil_opciones,
  { label: "Promedio movil", value: 6}
);
const movil_meses = Generators.input(movil_meses_input);

//  Grafico
function mostrarGrafico1(data, width) {
  return Plot.plot({
    marginBottom: 75,
    marginLeft: 45,
    marginRight: 65,
    width: width,
    x: {tickRotate: -90},
    y: {grid: true, label: "Porcentaje"},
    color: {legend: true},
    marks: [
      Plot.ruleY([0]),
      Plot.lineY(data, {x: "FECHA", y: "PROMEDIO_MOVIL", stroke:"PREGUNTA_NOM", tip:true, strokeWidth: 3, curve: "monotone-x"}),
      Plot.text(data, Plot.selectLast({x: "FECHA", y: "PROMEDIO_MOVIL", z: "PREGUNTA_NOM", text: "PREGUNTA_NOM", textAnchor: "start", dx:5, dy: 0, fill: "PREGUNTA_NOM", textOverflow:'ellipsis', lineWidth:8}))
    ],

  })
}
```

<div class="card">
  <h2>GRÁFICO N° 01 <br> PERÚ: PRINCIPALES PROBLEMAS DEL PAÍS</h2>
  <h3>(Porcentaje)</h3>
  <h3>${ movil_nombres.get(movil_meses) }: ${ year_inicio } - ${ year_fin }</h3>

  <!-- Filtros -->
  <div>

  ${ view(year_inicio_input) }
  ${ view(year_fin_input) }
  ${ view(movil_meses_input) }
  </div>

  <!-- Grafico -->
  <div>
  ${ resize(w=>mostrarGrafico1(problemasFiltrado,w)) }
  </div>

  <h3>Fuente: Instituto Nacional de Estadistica e Informatica. 
    ENAHO (Modulo: Gobernabilidad, Transparencia y Democracia)</h3>
</div>


## 2 y 3. La corrupción, según características demográficas

```sql id=corrupcion
   SELECT * FROM corrupcion 
    WHERE P23 = 'SI' 
    AND (Periodo = ${selector1} OR Periodo = ${selector2})
```
```sql id=opciones
   SELECT DISTINCT Periodo FROM corrupcion 
   WHERE RIGHT(Periodo,3) != 'CV%'
   ORDER BY SUBSTRING(Periodo,5,4) ASC
```
```sql id=problemasFiltrado2
   SELECT * FROM gestion_gobierno
   WHERE (Periodo = ${selector5} OR Periodo = ${selector6})
   AND ZONA = ${selector3}
```
```sql id=opciones2
   SELECT DISTINCT ZONA FROM gestion_gobierno
```
```sql id=opciones4
   SELECT DISTINCT Periodo FROM gestion_gobierno
```

```js
// Grafico 03
const opciones1 = JSON.parse(opciones);
const selectOptions = opciones1.map(d => d.Periodo);
const selectElement_input = Inputs.select(selectOptions, { label: "Primer Periodo" });
const selector1 = Generators.input(selectElement_input);

const selectElement2_input = Inputs.select(selectOptions, { label: "Segundo Periodo" });
const selector2 = Generators.input(selectElement2_input);


// Grafico 05
const opciones3 = JSON.parse(opciones2);
const selectOptions3 = opciones3.map(d => d.ZONA);
const selectElement3_input= Inputs.select(selectOptions3, { label: "Region", value: "NACIONAL" });
const selector3 = Generators.input(selectElement3_input);

const opciones5  = JSON.parse(opciones4);
const selectOptions5 = opciones5.map(d => d.Periodo);
const selectElement_input5 = Inputs.select(selectOptions5, { label: "Primer Periodo" });

const selector5 = Generators.input(selectElement_input5);

const selectElement_input6 = Inputs.select(selectOptions5, { label: "Segundo Periodo" });
const selector6 = Generators.input(selectElement_input6);


function mostrarGrafico2_2(data,opciones,opciones4, width){
    //const filteredData = data.filter(d => d.VARIABLE === "ZONA");
    const datos = JSON.parse(data);
    const filteredData = datos.filter(d => d.VARIABLE === "ZONA");
    const filteredData2 = datos.filter(d => d.VARIABLE === "SEXO");
    const filteredData3 = datos.filter(d => d.VARIABLE === "NIVEL EDUCATIVO");
    const ordenFx = ["URBANO","RURAL","HOMBRE","MUJER","PRIMARIA","SECUNDARIA","SUPERIOR"]
    return Plot.plot({
        width: width,
        x: {axis:null, tickRotate: 0},            
        y: {grid: true}, 
        color: { legend: true, scheme:"ylgnbu"},
        marks: [
            Plot.barY(filteredData, {y: "Valor",x: "Periodo", stroke: "Periodo",fill: "Periodo",fx:"VARIABLE_2",sort: {x: "y"}}),
            Plot.text(filteredData, {x: "Periodo", y: "Valor", fx:"VARIABLE_2", text: (d) => d.Valor, dy: -6, lineAnchor: "bottom"}),
            Plot.barY(filteredData2, {y: "Valor",x: "Periodo", stroke: "Periodo",fill: "Periodo",fx:"VARIABLE_2",sort: {x: "y"}}),
            Plot.text(filteredData2, {x: "Periodo", y: "Valor", fx:"VARIABLE_2", text: (d) => d.Valor, dy: -6, lineAnchor: "bottom"}),
            Plot.barY(filteredData3, {y: "Valor",x: "Periodo", stroke: "Periodo",fill: "Periodo",fx:"VARIABLE_2",sort: {x: "y"}}),
            Plot.text(filteredData3, {x: "Periodo", y: "Valor", fx:"VARIABLE_2", text: (d) => d.Valor, dy: -6, lineAnchor: "bottom"}),
            Plot.ruleY([0])
        ],
        fx: {
            domain: ordenFx // Aplicar el dominio ordenado
        },
    })
}

function mostrarGrafico2(data,opciones2,opciones3){  
    const datos = JSON.parse(data);
    console.log(datos)

    const filteredData = datos.filter(d => d.PREGUNTA === "GOBIERNO CENTRAL")
    const filteredData2 = datos.filter(d => d.PREGUNTA === "GOBIERNO REGIONAL")
    const filteredData3 = datos.filter(d => d.PREGUNTA === "GOBIERNO LOCAL")
    //console.log(filteredData3)
    return [
        Plot.plot({
            width:550,
            height:500,
            x: {tickRotate: 0,label:"Gobierno Central"},            
            y: {grid: true,axis:null}, 
            color: { legend: true, scheme:"ylgnbu"},
            marks: [
                Plot.barY(filteredData, {y: "Valor",x: "OPINION DE LA POBLACION", stroke: "OPINION DE LA POBLACION",fill: "OPINION DE LA POBLACION",fx:"Periodo", style: { text: {display:"none"} }, strokewidth:0.3, sort: {x: "y"}}),
                Plot.text(filteredData, {x: "OPINION DE LA POBLACION", y: "Valor", fx:"Periodo", text: (d) => d.Valor, dy: -6, lineAnchor: "bottom"}),
                Plot.ruleY([0])
            ],
        }),
        Plot.plot({
            width:550,
            height:540,
            x: {tickRotate: 0,label:"Gobierno Regional"},            
            y: {grid: true,axis:null}, 
            color: { scheme:"ylgnbu"},
            marks: [
                Plot.barY(filteredData2, {y: "Valor",x: "OPINION DE LA POBLACION", stroke: "OPINION DE LA POBLACION",fill: "OPINION DE LA POBLACION",fx:"Periodo",sort: {x: "y"} }),
                Plot.text(filteredData2, {x: "OPINION DE LA POBLACION", y: "Valor", fx:"Periodo", text: (d) => d.Valor, dy: -6, lineAnchor: "bottom"}),
                Plot.ruleY([0])
            ],
        }),
        Plot.plot({
            width:550,
            height: 540,
            x: {tickRotate: 0,label:"Gobierno Local"},            
            y: {grid: true,axis:null}, 
            color: {  scheme:"ylgnbu"},
            marks: [
                Plot.barY(filteredData3, {y: "Valor",x: "OPINION DE LA POBLACION", stroke: "OPINION DE LA POBLACION",fill: "OPINION DE LA POBLACION",fx:"Periodo",sort: {x: "y"}}),
                Plot.text(filteredData3, {x: "OPINION DE LA POBLACION", y: "Valor", fx:"Periodo", text: (d) => d.Valor, dy: -6, lineAnchor: "bottom"}),
                Plot.ruleY([0])

            ],
        }),       
    ]
}
```

```sql id=corrupcion_1Filtrado
SELECT PERIODO_INICIO, PERIODO_FIN, PERIODO_SEMESTRE_MOVIL,Porcentaje_100,ZONA FROM corrupcion_1 
WHERE PERIODO_SEMESTRE_MOVIL >= ${selector1_1} AND PERIODO_SEMESTRE_MOVIL <= ${selector2_1}
```

```sql id=opciones_corrupcion_1
   SELECT DISTINCT PERIODO_SEMESTRE_MOVIL FROM corrupcion_1 
```

```js
const opciones_corrupcion_1_1 = JSON.parse(opciones_corrupcion_1);
const selectOptions_1_2 = opciones_corrupcion_1_1.map(d => d.PERIODO_SEMESTRE_MOVIL); 
const selectElement_input_1 = Inputs.select(selectOptions_1_2, { label: "Desde", value: '2022-04 a 2022-09' });
const selector1_1 = Generators.input(selectElement_input_1);

const selectOptions_2_1 = opciones_corrupcion_1_1.map(d => d.PERIODO_SEMESTRE_MOVIL); 
const selectElement2_input_1 = Inputs.select(selectOptions_1_2, { label: "Hasta", value: '2023-07 a 2023-12' });
const selector2_1 = Generators.input(selectElement2_input_1);

function mostrarGrafico2_1(data, width){
    return Plot.plot({
        marginBottom: 100,
        marginRight: 60,
        width: width,
        x: {tickRotate: -45, label:'Periodo', },
        y: {grid: true, label: "Porcentaje"},
        color: {legend: true,},
        marks: [
            Plot.ruleY([0]),
            Plot.lineY(data, {x: "PERIODO_SEMESTRE_MOVIL", y: "Porcentaje_100", stroke:"ZONA", tip:true, strokeWidth: 3, curve: "monotone-x"}),
            Plot.dot(data, { x: "PERIODO_SEMESTRE_MOVIL", y: "Porcentaje_100", fill: "ZONA" }),
            Plot.text(data, {
                x: "PERIODO_SEMESTRE_MOVIL",
                y: "Porcentaje_100",
                text: d => d.Porcentaje_100,
                dx: 9, // Desplazamiento en X
                dy: -9, // Desplazamiento en Y
                fill: "ZONA",
                fontSize: 10
            }),
            Plot.text(data, Plot.selectLast({x: "PERIODO_SEMESTRE_MOVIL", y: "Porcentaje_100", z: "ZONA", text: "ZONA", textAnchor: "start", dx:7, dy: 0, fill: "ZONA", textOverflow:'ellipsis', lineWidth:8}))
        ],
    })
}
```

<div class="grid grid-cols-2">
  <div class="card">
      <h2>GRÁFICO N° 02 <br> PERÚ: CORRUPCION, SEGUN AREA DE RESIDENCIA</h2>
      <h3>Semestre Movil (Porcentaje)</h3><br>
      <h4>SI LE SOLICITARON "UN PAGO EXTRA"</h4>
      ${view(selectElement_input_1)}
      ${view(selectElement2_input_1)}
      ${ resize(width=>mostrarGrafico2_1(corrupcion_1Filtrado, width)) }
      <h3>Fuente: Instituto Nacional de Estadistica e Informatica. 
      ENAHO (Modulo: Gobernabilidad, Transparencia y Democracia)</h3>
  </div>


  <div class="card">
    <h2>GRÁFICO N° 03 <br> PERÚ: CORRUPCIÓN, SEGÚN CARACTERÍSTICAS DEMOGRÁFICAS</h2>
    <h3>Semestre Movil (Porcentaje)</h3><br>
    <h4>SI LE SOLICITARON "UN PAGO EXTRA"</h4>
${view(selectElement_input)}
${view(selectElement2_input)}
    <div>
${ resize(width=>mostrarGrafico2_2(corrupcion,opciones,null,width)) }
    </div>
    <h3>Fuente: Instituto Nacional de Estadistica e Informatica. 
    ENAHO (Modulo: Gobernabilidad, Transparencia y Democracia)</h3>
  </div>

</div>



## 4. Nivel de confianza en las instituciones

```sql id=entidadesFiltrado
SELECT
  *
FROM (
  SELECT
    *
  FROM entidades
  WHERE Periodo like ${movil_semestre_entidades}
  ORDER BY
    CASE 
      WHEN Confianza = 'SUFICIENTE / BASTANTE' THEN 1
      WHEN Confianza = 'NADA / POCO' THEN 2
      WHEN Confianza = 'NO SABE' THEN 3
      ELSE 4 -- Opcional para manejar casos no especificados
    END
) AS P

```

```js
// Inputs
const periodos_entidades = JSON.parse(await sql`SELECT DISTINCT Periodo AS periodos_entidades FROM entidades ORDER BY Mes`).map(o=>o.periodos_entidades)

const movil_semestre_entidades_input = Inputs.select(
  periodos_entidades,
  { label: "Semestre", value: 6}
);
const movil_semestre_entidades = Generators.input(movil_semestre_entidades_input);

//  Grafico
function mostrarGrafico3(data) {
  return Plot.plot({
    marginRight: 150,
    axis: null,

    color: {legend: "ramp", scheme: "tableau10", width: 340, label: "Confianza"},
    marks: [
      Plot.barX(data, Plot.stackX(
        {
          x: "Porcentaje",
          y:"Entidad",
          fill:"Confianza",
          tip:true,
          sort: {
            color: null,
            y: "-data",
            reduce: (D) => D.find((d) => d.Porcentaje)?.Porcentaje
          }
        }),
      ),
      Plot.text(data, Plot.stackX( {fill:"white", x: "Porcentaje", y:"Entidad", text: D => D.Porcentaje > 4? D.Porcentaje.toFixed(2) : ""} )),
      
      Plot.text(data, Plot.selectLast({x: 100, y: "Entidad", z: "Entidad", text: "Entidad", textAnchor: "start", dx:5, dy: 0, textOverflow:'ellipsis', lineWidth:15}))
    ]
  })
}
```

<div class="card">
  <h2>GRÁFICO N° 04 <br> PERÚ: NIVEL DE CONFIANZA EN LAS INSTITUCIONES</h2>
  <h3>(Porcentaje)</h3>
  <h3>Semestre: ${movil_semestre_entidades}</h3>

  <!-- Filtros -->
  <div>

  ${ view(movil_semestre_entidades_input) }
  </div>

  <!-- Grafico -->
  <div>
  ${ display(mostrarGrafico3(entidadesFiltrado)) }
  </div>

  <h3>Fuente: Instituto Nacional de Estadistica e Informatica. 
    ENAHO (Modulo: Gobernabilidad, Transparencia y Democracia)</h3>
</div>


## 5. Gestión de los Gobiernos centrales, regionales y locales

<div class="card" >
    <h2>GRAFICO N° 05 <br> GESTION DEL GOBIERNO CENTRAL, REGIONAL Y LOCAL</h2>
    <h3>Semestre Movil (Porcentaje)</h3><br>
    ${view(selectElement3_input)}
    ${view(selectElement_input5)}
    ${view(selectElement_input6)}
    <div style="display:flex;">
        ${ mostrarGrafico2(problemasFiltrado2,opciones2)}
    </div>
    <h3>Fuente: Instituto Nacional de Estadistica e Informatica. 
    ENAHO (Modulo: Gobernabilidad, Transparencia y Democracia)</h3>
</div>


## 6. ¿La democracia sirve para elegir autoridades?

```js
// Inputs
const movil_semestre_elec_democracia_input = Inputs.select(
  JSON.parse(await sql`SELECT DISTINCT Periodo AS periodos_elec_democracia FROM democraciaElecciones`)
  .map(o=>o.periodos_elec_democracia),
  { label: "Semestre" }
);
const movil_semestre_elec_democracia = Generators.input(movil_semestre_elec_democracia_input);

// Datos
const departamentos = await FileAttachment("data/peru_departamental_simple.geojson").json()
const db_democracia_elec = await FileAttachment("data/grafico6_dataloader.json").json()


// Grafico
function mostrarGrafico6(filtroPeriodo, width) {

  // Filtros
  let departamentosGeoJSON = JSON.parse(JSON.stringify(departamentos))
  for (let feature of departamentosGeoJSON['features']) {
    
    
    for (let registro of db_democracia_elec){
      if (
        registro.Departamento == feature.properties.NOMBDEP
        && registro.Periodo == filtroPeriodo
      ){
        //console.log(registro)
        feature.properties['Porcentaje'] = registro.Porcentaje
        break
      }

    }
  }

  return Plot.plot({
    width: width,
    projection: { type: "mercator", domain: departamentos },
    color: {
      //type: "quantile",
      //n:/ 9,
      scheme: "brbg",
      legend: true,
      type: "linear",
      domain: [0,100]
    },
    marks: [
      Plot.geo(departamentosGeoJSON, {
        tip: true,
        stroke: "white",
        title: (d) => `${d.properties.NOMBDEP} ${d.properties.Porcentaje.toFixed(2)}%`,
        fill: "Porcentaje"
      }),
      Plot.text(departamentosGeoJSON, Plot.centroid({ text: "NOMBDEP", dy: -10, fontWeight: "bold" })),
      Plot.text(departamentosGeoJSON, Plot.centroid({ text:  (d) => `${d.properties.Porcentaje.toFixed(2)}%` }))

    ]
  })
}

/*

Codigo con leaflet

const div = display(document.createElement("div"));
div.style = "height: 400px;";

const map = L.map(div)
  .setView([51.505, -0.09], 13);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


L.geoJson(departamentos).addTo(map);
*/
  
```

<div class="card">
  <h2>GRÁFICO N° 6 <br> PERÚ:¿LA DEMOCRACIA SIRVE PARA ELEGIR AUTORIDADES?</h2>
  <h3>(Porcentaje)</h3>
  <h3>Semestre: ${movil_semestre_elec_democracia}</h3>

${ view(movil_semestre_elec_democracia_input) }
${ resize(w=>mostrarGrafico6( movil_semestre_elec_democracia, w ) ) }

  <h3>Fuente: Instituto Nacional de Estadistica e Informatica. 
    ENAHO (Modulo: Gobernabilidad, Transparencia y Democracia)</h3>
</div>