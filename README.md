# Dashboard Interactivo para Indicadores del Módulo de Gobernabilidad, Democracia y Transparencia

Este proyecto desarrolla un dashboard interactivo utilizando Observable Framework para la visualización de indicadores clave del Módulo 85 de la Encuesta Nacional de Hogares (ENAHO). El dashboard permite explorar de manera dinámica los datos relacionados con gobernabilidad, democracia y transparencia en Perú.

## **Descripción**

El Módulo de Gobernabilidad, Democracia y Transparencia de la ENAHO recoge información clave sobre la percepción ciudadana respecto a instituciones, corrupción, democracia, y otros aspectos críticos. Este proyecto busca:

- Mejorar la accesibilidad y comprensión de los datos.
- Facilitar el análisis de tendencias y patrones regionales.
- Promover un diálogo informado entre sociedad y gobierno.

El dashboard presenta indicadores como la confianza en instituciones, percepción de la corrupción, y gestión del gobierno, mediante gráficos interactivos con filtros personalizables.

## **Características**

- Visualización de 6 indicadores principales sobre gobernabilidad, democracia y transparencia.
- Gráficos dinámicos con opciones de filtrado por:
  - Región.
  - Área de residencia.
  - Periodo de tiempo.
- Comparación de tendencias y análisis demográfico.
- Escalabilidad para incorporar nuevos indicadores o módulos de la ENAHO.

### **Herramientas Utilizadas**
- **Python (Pandas):** Limpieza y transformación de datos.
- **Observable Framework:** Desarrollo de visualizaciones interactivas.
- **Google Colab:** Ejecución de scripts.
- **GitHub:** Control de versiones y colaboración en el código.

## **Indicadores**

1. **Principales problemas del país:** Identificación de los problemas más relevantes percibidos por la población.
2. **Corrupción:** Evaluación del porcentaje de hogares afectados por actos de corrupción.
3. **Confianza en instituciones:** Percepción de la población sobre la legitimidad de las instituciones clave.
4. **Gestión gubernamental:** Opinión pública sobre la gestión a nivel central, regional y local.
5. **Utilidad de la democracia para elegir gobernantes:** Opinión sobre la eficacia del sistema democrático en la elección de autoridades.
6. **Funcionamiento de la democracia:** Percepción de la calidad del sistema democrático.

## **Fuente de Datos**

El dashboard utiliza datos del Módulo 85 de la ENAHO (2007-2024) también datos sobre gobernabilidad extraidos de DATACRIM.

## **Colaboradores**

- Allison Regina Torres Lazo  
- Cynthya Vanessa Cevallos Mamani  
- Deivid Stewart Ramirez Castillo  
- Emerson Jamil Quispe Goicochea  
- Gian Carlo Orcotoma Mormontoy  

## **Como ver el dashboard**

Puede ver el dashboard en funcionamiento aqui: https://inei-dashboard.observablehq.cloud/enaho-dashboard/

## **Como utilizar este proyecto**

Si lo que deseas es ejecutar el código fuente, necesitarás los siguientes requisitos instalados en tu computadora para asegurar la replicabilidad del proyecto.
| Herramienta   | Versión   | Notas                   |
|---------------|-----------|-------------------------|
| Node          | 18.17.0   |                         |
| npm           | 9.6.7     |                         |
| Python        | 3.12.2    |                         |
| pandas        | 2.2.3     | Librería de Python      |
| numpy         | 2.1.3     | Librería de Python      |

Esta es una aplicación de Observable Framework, así que una vez clonado el repositorio deberás instalar las dependencias requeridas, ejecuta:

```bash
npm install
```
Luego, para iniciar el servidor de vista previa local, ejecuta:

```bash
npm run dev
```
Luego visita http://localhost:3000 para previsualizar el dashboard.
