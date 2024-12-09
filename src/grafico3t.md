---
title: grafico3t
theme: glacier
toc: false
sql:
  problemas: data/grafico3_dataloader.json
  gestion_gobierno: data/grafico5_dataloader.json
---

```sql id=problemasFiltrado
   SELECT * FROM problemas 
    WHERE P23 = 'SI' 
    AND (Periodo = ${selector1} OR Periodo = ${selector2})
```
```sql id=opciones
   SELECT DISTINCT Periodo FROM problemas 
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
const selectElement3_input= Inputs.select(selectOptions3, { label: "Region" });
const selector3 = Generators.input(selectElement3_input);

const opciones5  = JSON.parse(opciones4);
const selectOptions5 = opciones5.map(d => d.Periodo);
const selectElement_input5 = Inputs.select(selectOptions5, { label: "Primer Periodo" });
const selector5 = Generators.input(selectElement_input5);

const selectElement_input6 = Inputs.select(selectOptions5, { label: "Segundo Periodo" });
const selector6 = Generators.input(selectElement_input6);


function mostrarGrafico(data,opciones,opciones4){
    //const filteredData = data.filter(d => d.VARIABLE === "ZONA");
    const datos = JSON.parse(data);
    const filteredData = datos.filter(d => d.VARIABLE === "ZONA");
    const filteredData2 = datos.filter(d => d.VARIABLE === "SEXO");
    const filteredData3 = datos.filter(d => d.VARIABLE === "NIVEL EDUCATIVO");
    const ordenFx = ["URBANO","RURAL","HOMBRE","MUJER","PRIMARIA","SECUNDARIA","SUPERIOR"]
    return Plot.plot({
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
        })
    ]
}
```

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


<div class="card" >
    <h2>GRÁFICO N° 03 <br> PERÚ: CORRUPCION, SEGUN CARACTERISTICAS DEMOGRAFICAS</h2>
    <h3>Semestre Movil (Porcentaje)</h3><br>
    <h4>SI LE SOLICITARON "UN PAGO EXTRA"</h4>
    ${view(selectElement_input)}
    ${view(selectElement2_input)}
    <div>
        ${mostrarGrafico(problemasFiltrado,opciones)}
    </div>
   <h3>Fuente: Instituto Nacional de Estadistica e Informatica. 
    ENAHO (Modulo: Gobernabilidad, Transparencia y Democracia)</h3>
</div>

