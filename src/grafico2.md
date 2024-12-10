---
title: grafico2
theme: air
toc: false
sql:
  corrupcion_1: data/grafico2_dataloader.json
---

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

function mostrarGrafico2_1(data){
    return Plot.plot({
        marginBottom: 120,
        marginRight: 60,
        width: width,
        x: {tickRotate: -90, label:'Periodo', },
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
<div class="card">
    <h2>GRÁFICO N° 02 <br> PERÚ: CORRUPCION, SEGUN AREA DE RESIDENCIA</h2>
    <h3>Semestre Movil (Porcentaje)</h3><br>
    <h4>SI LE SOLICITARON "UN PAGO EXTRA"</h4>
    ${view(selectElement_input_1)}
    ${view(selectElement2_input_1)}
    ${mostrarGrafico2_1(corrupcion_1Filtrado)}
    <h3>Fuente: Instituto Nacional de Estadistica e Informatica. 
    ENAHO (Modulo: Gobernabilidad, Transparencia y Democracia)</h3>
</div>
