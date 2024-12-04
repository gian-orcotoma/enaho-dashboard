---
theme: glacier
toc: false
sql:
  problemas: data/grafico1_dataloader.json
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
  AND AÑO <= ${year_fin};
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
    marginRight: 60,
    width: width,
    x: {tickRotate: -90},
    y: {grid: true, label: "Porcentaje"},
    color: {legend: true},
    marks: [
      Plot.ruleY([0]),
      Plot.lineY(data, {x: "FECHA", y: "PROMEDIO_MOVIL", stroke:"PREGUNTA_NOM", tip:true}),
      Plot.text(data, Plot.selectLast({x: "FECHA", y: "PROMEDIO_MOVIL", z: "PREGUNTA_NOM", text: "PREGUNTA_NOM", textAnchor: "start", dx:1, dy: 0, fill: "PREGUNTA_NOM", textOverflow:'ellipsis', lineWidth:8}))
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

## 2. 
<div class="card">
  <h2><br></h2>
  <h3></h3>
  <h3></h3>

  <!-- Filtros -->
  <div>
  </div>

  <!-- Grafico -->
  <div>
  </div>
</div>