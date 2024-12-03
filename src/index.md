---
theme: dashboard
toc: false
---

<div class="hero">
  <h1>.\enaho-dashboard</h1>
  <h2>Welcome to your new app! Edit&nbsp;<code style="font-size: 90%;">src/index.md</code> to change this page.</h2>
  <a href="https://observablehq.com/framework/getting-started">Get started<span style="display: inline-block; margin-left: 0.25rem;">↗︎</span></a>
</div>


<!-- GRÁFICO N° 01PERÚ: PRINCIPALES PROBLEMAS DEL PAÍS -->
```js
//////////////////////////////// Inputs
const añoInput = Inputs.range([2014, 2024], {label: "Año:", step:1, value:2023});
const año = Generators.input(añoInput);

const corteInput = Inputs.select(
  ['TRIMESTRE', 'SEMESTRE', 'FECHA'],
  {
    label: "Grupo"
  }
);
const cortes = Generators.input(corteInput);


//////////////////////////////// Data
const problemas = await FileAttachment("data/grafico1_dataloader.json").json();

function filtrarProblemas(dataset, fecha_inicio='0000-00', fecha_fin='9999-99') {
  let data = dataset['data']

  data = data.filter((registro)=>{
    registro['FECHA'] >= fecha_inicio &&
    registro['FECHA'] <= fecha_fin
  })

  // Generar grupos de meses por año
  /*
  let meses_en_grupo = Math.floor(12 / grupos)
  let datos_agrupados = []

  for (let registro of data){
    let fecha = registro['AÑO']
    let grupo = Math.floor((registro['MES'] - 1) / meses_en_grupo) + 1
    fecha = fecha += grupo.toString().padStart(2, '0')

    let nuevo = registro
    nuevo['FECHA'] = fecha

    datos_agrupados.push(nuevo)
  }
  */

  return data
}

const problemas_filtrado = filtrarProblemas(problemas, '0000-00', '9999-99')

//////////////////////////////// Grafico
function mostrarGrafico1(data) {
  return Plot.plot({
    width: width,
    x: {tickRotate: -90},
    y: {grid: true, label: "Porcentaje"},
    marks: [
      Plot.ruleY([0]),
      Plot.lineY(data, {x: "FECHA", y: "VALOR", stroke:"PREGUNTA_NOM", tip: true}),
      Plot.text(data, Plot.selectLast({x: "FECHA", y: "VALOR", z: "PREGUNTA_NOM", text: "PREGUNTA_NOM", textAnchor: "start", dx: 3}))
    ]
  })
}

```

<div class="card">
  <h2>GRÁFICO N° 01 PERÚ: PRINCIPALES PROBLEMAS DEL PAÍS</h2>
  <h3>Porcentaje</h3>

  <!-- Filtros -->
  <div>
  ${ resize((width) => añoInput) }
  ${ resize((width) => corteInput) }
  </div>

  <!-- Grafico -->
  <div>
    ${ resize((width) => mostrarGrafico1(problemas['data'])) }
  </div>
</div>










---

## Next steps

Here are some ideas of things you could try…

<div class="grid grid-cols-4">
  <div class="card">
    Chart your own data using <a href="https://observablehq.com/framework/lib/plot"><code>Plot</code></a> and <a href="https://observablehq.com/framework/files"><code>FileAttachment</code></a>. Make it responsive using <a href="https://observablehq.com/framework/javascript#resize(render)"><code>resize</code></a>.
  </div>
  <div class="card">
    Create a <a href="https://observablehq.com/framework/project-structure">new page</a> by adding a Markdown file (<code>whatever.md</code>) to the <code>src</code> folder.
  </div>
  <div class="card">
    Add a drop-down menu using <a href="https://observablehq.com/framework/inputs/select"><code>Inputs.select</code></a> and use it to filter the data shown in a chart.
  </div>
  <div class="card">
    Write a <a href="https://observablehq.com/framework/loaders">data loader</a> that queries a local database or API, generating a data snapshot on build.
  </div>
  <div class="card">
    Import a <a href="https://observablehq.com/framework/imports">recommended library</a> from npm, such as <a href="https://observablehq.com/framework/lib/leaflet">Leaflet</a>, <a href="https://observablehq.com/framework/lib/dot">GraphViz</a>, <a href="https://observablehq.com/framework/lib/tex">TeX</a>, or <a href="https://observablehq.com/framework/lib/duckdb">DuckDB</a>.
  </div>
  <div class="card">
    Ask for help, or share your work or ideas, on our <a href="https://github.com/observablehq/framework/discussions">GitHub discussions</a>.
  </div>
  <div class="card">
    Visit <a href="https://github.com/observablehq/framework">Framework on GitHub</a> and give us a star. Or file an issue if you’ve found a bug!
  </div>
</div>

<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 8rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 1rem 0;
  padding: 1rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>
