---
toc: false
sql:
  problemas: data/grafico1_dataloader.json
  entidades: data/grafico4_dataloader.json
  democraciaElecciones: data/grafico6_dataloader.json
  democraciaElecciones2: data/grafico6_dataloader.json
---
# Dashboard de Percepcion Ciudadana

<div class="grid grid-cols-4">
  <div class="card" style="color: inherit;">
    <h2>Principal problema del país</h2>
    <span class="big">Corrupción</span>
  </div>
</div>


<!-- GRÁFICO N° 01PERÚ: PRINCIPALES PROBLEMAS DEL PAÍS -->
```sql id=problemasFiltrado
SELECT * FROM(
  SELECT * FROM (
    SELECT
      VALOR
      ,AÑO
      ,FECHA
      ,PREGUNTA_NOM
      ,PREGUNTA_COD
      ,AVG(VALOR) OVER (
        PARTITION BY PREGUNTA_COD
        ORDER BY FECHA
        ROWS BETWEEN ${movil_meses-1} PRECEDING AND CURRENT ROW
      ) AS PROMEDIO_MOVIL
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
      ,AVG(VALOR) OVER (
        PARTITION BY PREGUNTA_COD
        ORDER BY FECHA
        ROWS BETWEEN ${movil_meses-1} PRECEDING AND CURRENT ROW
      ) AS PROMEDIO_MOVIL
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
const [{max_year}] = await sql`select max(AÑO) as max_year from problemas`
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
function mostrarGrafico1(data) {
  return Plot.plot({
    marginBottom: 75,
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
## 1. Los principales problemas del pais
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
  ${ display(mostrarGrafico1(problemasFiltrado)) }
  </div>
</div>





<!-- GRÁFICO N° 04 PERÚ: PRINCIPALES PROBLEMAS DEL PAÍS -->
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
## 4. Nivel de confianza en las instituciones
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
</div>





<!-- GRÁFICO N° 17 PERÚ: PRINCIPALES PROBLEMAS DEL PAÍS -->
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
function mostrarGrafico6(filtroPeriodo) {

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
    projection: { type: "mercator", domain: departamentos },
    color: {
      //type: "quantile",
      //n:/ 9,
      scheme: "rdbu",
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

## 6. ¿La democracia sirve para elegir autoridades?
<div class="grid grid-cols-2">

  <div class="card">
    <h2>GRÁFICO N° 6 <br> PERÚ:¿LA DEMOCRACIA SIRVE PARA ELEGIR AUTORIDADES?</h2>
    <h3>(Porcentaje)</h3>
    <h3>Semestre: ${movil_semestre_elec_democracia}</h3>

${ view(movil_semestre_elec_democracia_input) }
${ display( mostrarGrafico6( movil_semestre_elec_democracia ) ) }

  </div>
</div>


