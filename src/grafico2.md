---
title: grafico2
theme: glacier
toc: false
sql:
  problemas: data/grafico2_dataloader.json
---

# Dashboard de Percepcion Ciudadana
<div class="grid grid-cols-4">
  <div class="card" style="color: inherit;">
    <h2>Principal problema del país</h2>
    <span class="big">Corrupción</span>
  </div>
</div>

<!-- GRÁFICO N° 01PERÚ: PRINCIPALES PROBLEMAS DEL PAÍS -->
# Dashboard de Percepcion Ciudadana

<div class="grid grid-cols-4">
  <div class="card" style="color: inherit;">
    <h2>Principal problema del país</h2>
    <span class="big">Corrupción</span>
  </div>
</div>


<!-- GRÁFICO N° 01PERÚ: PRINCIPALES PROBLEMAS DEL PAÍS -->
```sql id=problemasFiltrado
   SELECT B.AÑO,B.MES,B.AÑOMES,B.ZONA,ROUND((B.SUMA_SI/B.TOTAL)*100,2) AS PORCENTAJE_SI
    FROM (
        SELECT A.AÑO,A.AÑOMES,A.MES,A.ZONA, SUM(CASE WHEN A.PAGO_EXTRA = 'No' OR A.PAGO_EXTRA is NULL THEN A.FACTOR07 ELSE 0 END) SUMA_NO,SUM(CASE WHEN A.PAGO_EXTRA = 'Si' THEN A.FACTOR07 ELSE 0 END) SUMA_SI, A.TOTAL FROM (
            SELECT AÑO,MES AS AÑOMES,MES,CONCAT(AÑO,MES),ZONA,PAGO_EXTRA,FACTOR07,SUM(FACTOR07) OVER (PARTITION BY CONCAT(AÑO,MES_NOMBRE),ZONA) AS TOTAL
            FROM problemas
            WHERE P23 IS NOT NULL
            ORDER BY AÑO,MES
        ) A 
        GROUP BY A.AÑOMES,A.ZONA,A.TOTAL,A.MES,A.AÑO
    ) B 
    WHERE B.AÑO >= ${year_inicio} AND B.AÑO <= ${year_fin}
    GROUP BY B.AÑOMES,B.ZONA,B.SUMA_SI,B.TOTAL,B.MES,B.AÑO
    UNION ALL
    SELECT  AÑO,MES,MES AS AÑOMES,'Total',ROUND((SUM(CASE WHEN PAGO_EXTRA = 'Si' THEN FACTOR07 ELSE 0 END)/SUM(FACTOR07))*100,2) PORCENTAJE_SI
    FROM problemas                
    WHERE P23 IS NOT NULL 
    GROUP BY AÑO,MES,'Total'
```

```js
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

function mostrarGrafico1(data) {
  return Plot.plot({
    marginBottom: 75,
    marginRight: 60,
    width: width,
    x: {tickRotate: -90, label:'Periodo'},
    y: {grid: true, label: "Porcentaje"},
    color: {legend: true},
    marks: [
      Plot.ruleY([0]),
      Plot.lineY(data, {x: "MES", y: "PORCENTAJE_SI", stroke:"ZONA", tip:true}),
      Plot.dot(data, { x: "MES", y: "PORCENTAJE_SI", fill: "ZONA" }),
      Plot.text(data, {
      x: "MES",
      y: "PORCENTAJE_SI",
      text: d => d.PORCENTAJE_SI,
      dx: 9, // Desplazamiento en X
      dy: -9, // Desplazamiento en Y
      fill: "ZONA",
      fontSize: 10
    }),
      Plot.text(data, Plot.selectLast({x: "MES", y: "PORCENTAJE_SI", z: "ZONA", text: "ZONA", textAnchor: "start", dx:1, dy: 0, fill: "ZONA", textOverflow:'ellipsis', lineWidth:8}))
    ],
  })
}
```
<div class="card">
  ${ view(year_inicio_input) }
  ${ view(year_fin_input) }
  ${ mostrarGrafico1(problemasFiltrado) }
</div>