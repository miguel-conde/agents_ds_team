
# Situacion actual y plan para montar un “Data Science Team” de agentes

## 1) Qué hay ahora en tu `.github/` (y qué podemos reutilizar tal cual)

En el repo tienes:

* `.github/agents/`

  * `router.agent.md` (orquestador)
  * `tech-specialist.agent.md`
  * `business-specialist.agent.md`
  * `creative-specialist.agent.md`
  * `data-specialist.agent.md`
  * `validator.agent.md`
* `.github/skills/planning-workflows/`

  * `SKILL.md`, `README.md`
  * `examples/plan-template.json` y ejemplos de planes
  * `reference/complexity-guidelines.md`, etc.

El patrón base funciona y es muy reutilizable:

* **Front-matter YAML** consistente (name/tools/agents/handoffs/model/target).
* **Handoffs** entre especialistas (con `send:false`, o sea, “sugerencias de colaboración” pero no “auto-dispatch”).
* **Skill de planning** con un template JSON y guías de complejidad.

Esto es exactamente lo que necesitamos para montar un “Data Science team” real, cambiando roles, contratos y Definition of Done.

---

## 2) Hallazgos y mejoras necesarias (tras leer tu router y skills)

### A) Tu router actual es demasiado “hands-off” para un Head of DS real

En tu router: “Never respond directly / only orchestrate”. Para un Head of DS esto te crea un problema: nadie “posee” decisiones (trade-offs) y el sistema tiende a bucles.

**Mejora**: mantener la delegación sistemática, pero el Head of DS debe tener:

* **Decision rights** (priorización, scope, riesgos aceptables)
* **Definition of Done** por tipo de entrega (dataset, modelo, despliegue, informe)
* **Interfaces / contratos** entre agentes para evitar solapes

### B) Tu skill de planning es buena, pero le falta tipado DS

`plan-template.json` incluye duración, stakeholders, criterios… bien.
Para DS/MLE/DE necesitamos además (obligatorio en proyectos reales):

* `deliverables[]` con `owner`, `paths`, `dod`, `reviewer`
* `data_contracts[]`
* `evaluation_protocol`
* `risks[]` (leakage, privacy, drift, reproducibilidad)
* `acceptance_criteria` medibles

---

## 3) Target: “Equipo DS” de agentes (roles + fronteras claras)

Vamos a crear (mínimo viable y serio):

1. **`head-of-ds-router`** (orquestador)
2. **`data-engineer`**
3. **`ml-engineer`**
4. **`data-scientist`**
5. **`validator`** (reutilizar el tuyo, pero con checklist DS/MLE/DE)

Opcional (si trabajas mucho con BI/semantic layer/dbt):

* **`analytics-engineer`** (pero solo si lo necesitas; por defecto, DE+DS suele bastar)

### Contratos (muy importantes)

* **DE → DS/MLE**: dataset + `data_contract` + tests DQ + runbook
* **DS → MLE**: feature spec + métrica(s) + split/validación + criterios de aceptación
* **MLE → Router**: pipeline reproducible + serving (si aplica) + monitoring + rollback

---

## 4) Plan de construcción (por fases, incremental y sin romper tu ejemplo)

### Fase 0 — Baseline y estructura

**Objetivo**: no romper el ejemplo, solo duplicarlo y evolucionarlo.

* Copiar `router.agent.md` → `head-of-ds-router.agent.md`
* Copiar `data-specialist.agent.md` → `data-scientist.agent.md` (y refinar)
* Copiar `tech-specialist.agent.md` → `ml-engineer.agent.md` (y refinar)
* Crear `data-engineer.agent.md` nuevo (partiendo de tech pero con foco datos)
* Mantener `validator.agent.md`, pero ampliarlo con validaciones DS

Deliverable: carpeta `.github/agents/` con los 5 agentes DS.

### Fase 1 — Skill de planning tipado para DS

**Objetivo**: que los proyectos DS “grandes” tengan plan robusto y verificable.

* Duplicar skill: `.github/skills/ds-planning-workflows/`
* Crear `plan-template-ds.json` con:

  * `deliverables[]` (owner/paths/dod)
  * `data_contracts[]`
  * `evaluation_protocol`
  * `mlops_requirements` (si aplica)
  * `risks[]`
  * `acceptance_criteria`

Deliverable: nueva skill y 2 ejemplos de planes reales:

* `plan-churn-prediction.json`
* `plan-mmm-pharma-bricks.json` (te viene al pelo por lo que estás trabajando)

### Fase 2 — Handoffs “de verdad” para DS (checkpoints)

En lugar de un único “Validate complex response”, crear 3 handoffs (muy prácticos):

1. `Validate Plan` (estructura, dependencias, DoD)
2. `Validate DS Output` (métricas, leakage, validación)
3. `Validate Prod Readiness` (reproducibilidad, tests, monitoring)

Deliverable: handoffs en el router y en validator (y si quieres, en MLE/DE).

### Fase 3 — Standards del repo (para que Copilot/agentes no improvisen)

Añadir `AGENTS.md` en raíz (o `.github/AGENTS.md`) como contrato:

* estilo Python, typing, testing, docstrings con ejemplo (tu preferencia)
* política notebooks → “explora en notebook, productiviza en `src/`”
* comandos canónicos (lint/test)
* criterio de PR “mergeable”

Deliverable: `AGENTS.md`.

### Fase 4 — Prueba de integración (1 caso end-to-end)

Elegimos un caso simple pero completo (recomendación):

* dataset tabular + pipeline + modelo + evaluación + empaquetado

El objetivo aquí es comprobar:

* que el router descompone bien
* que DE/DS/MLE no se pisan
* que validator detecta errores típicos

Deliverable: un “runbook” de demo + `plan-*.json` + artefactos.

---

## 5) Cambios concretos que haría en tus agentes (sin reescribir tu estilo)

### `head-of-ds-router.agent.md`

Mantener tu estructura, pero añadir 4 bloques:

1. **Decision Rights**

* define que el orquestador decide: scope, métrica primaria, criterios de aceptación, riesgo aceptable

2. **Definition of Done (DoD) por tipo**

* Dataset, Modelo offline, Modelo prod, Informe

3. **Interface contracts**

* DE→DS/MLE, DS→MLE, MLE→Router

4. **Fast-lane exception**

* permitir respuesta directa solo para: clarificación de requisitos y cuestiones triviales de ejecución/navegación

### `data-engineer.agent.md`

Debe ser “obsesivo” con:

* idempotencia, incremental, tests DQ, schemas, lineage
* “no inventar features”: implementa transformaciones acordadas con DS

### `data-scientist.agent.md`

Debe ser “obsesivo” con:

* baseline, métricas, validación (temporal si aplica), leakage checks
* convertir conclusiones en artefactos (feature spec + reporte)

### `ml-engineer.agent.md`

Debe ser “obsesivo” con:

* reproducibilidad (config/seeds), packaging, serving, monitoring
* tests “smoke” y rutas de inferencia

### `validator.agent.md`

Extender tu validator con checklist específico:

* leakage, contaminación train/test
* métricas mal definidas
* claims causales sin soporte
* reproducibilidad inexistente
* ausencia de DoD/acceptance criteria

# Ideas a considerar 

## 1) Nuevo Router: `head-of-ds-router` (orquestador)

### Cambios clave respecto a tu router

* Mantener el “single entry point”, pero añadir **Decision Rights**: el orquestador decide (y documenta) *qué se hace* y *qué no se hace*.
* Añadir un **Definition of Done (DoD)** estándar por tipo de entrega: dataset/pipeline, modelo, informe, deployment.
* Añadir **interfaces** entre agentes (contratos) para que no se pisen: DE entrega “dataset+schema+DQ”, DS entrega “feature spec + eval protocol”, MLE entrega “pipeline reproducible + serving/monitoring”.

### Front-matter sugerido

* `agents: ['data-engineer', 'ml-engineer', 'data-scientist', 'validator']`
* `tools`: mantén `todo`, `search`, `web`, `execute`, `edit`, `agent`

### Secciones nuevas que yo metería

* **Operating Cadence**:

  * “Discovery mode” → “Build mode” → “Productionize mode”.
* **Artifacts Registry**:

  * lista de artefactos por conversación: datasets, modelos, decisiones, métricas, rutas.
* **Risk register**:

  * leakage, bias, drift, privacy, compliance, reproducibilidad.

---

## 2) Agentes especialistas: responsabilidades y “entradas/salidas”

### A) `data-engineer`

**Misión**: convertir fuentes en datasets fiables y versionables.

**Inputs esperados**

* Fuente(s), periodicidad, SLA, llaves, granularidad, diccionario de variables.

**Outputs obligatorios**

* `data_contract` (schema + constraints)
* tests DQ (freshness, nulls, duplicados, rangos)
* pipeline (idempotente, incremental si aplica)
* “runbook” breve (cómo ejecutar)

**No hace**

* Feature engineering “model-driven” (eso lo lidera DS, aunque DE lo implemente si se acuerda).

---

### B) `data-scientist`

**Misión**: responder a la pregunta analítica y definir el protocolo de evaluación.

**Inputs**

* dataset (con contrato), objetivos de negocio, restricciones.

**Outputs obligatorios**

* baseline + métricas + split/validation (temporal si aplica)
* feature spec (qué features, transformaciones, leakage checks)
* análisis de errores / interpretabilidad mínima
* recomendaciones y “next experiments”

**No hace**

* Serving/CI/CD/MLOps (eso es MLE).

---

### C) `ml-engineer`

**Misión**: hacer que entrenar/servir/monitorizar sea una máquina repetible.

**Inputs**

* feature spec + evaluation protocol (DS)
* dataset contract + pipeline (DE)

**Outputs obligatorios**

* training pipeline reproducible (configs, seeds, tracking)
* inference path (batch/online) + tests smoke
* packaging, versioning, model registry (si existe)
* monitorización (drift + performance proxy)

**No hace**

* Storytelling de negocio (eso lo consolida el router, con apoyo DS).

---

### D) `validator`

Aquí lo reforzaría para DS:

* valida coherencia técnica y **consistencia artefacto↔texto**.
* checks de “common failure modes”: leakage, target encoding mal hecho, train/test contamination, métricas mal definidas, causal claims sin sustento, etc.

---

## 3) Handoffs: más específicos que “Validate Complex Response”

Te propongo 3 handoffs (mejor que uno genérico):

1. **`Validate Plan`** (cuando creas `plan-*.json`): ¿están bien definidos DoD, dependencias, owners, riesgos?
2. **`Validate DS Output`**: eval protocol, leakage checks, métricas y baseline.
3. **`Validate Production Readiness`**: reproducibilidad, tests, rollback plan, monitorización.

Esto te da checkpoints claros y evita que el validator sea “opinólogo”.

---

## 4) Planning files: en DS funcionan mejor si tipas el plan

En vez de `plan-[task].json` libre, usa una estructura estándar:

* `goal`
* `context`
* `deliverables[]` con `owner`, `dod`, `paths`
* `steps[]` con `dependencies`, `agent`, `inputs`, `outputs`, `verify`
* `risks[]`
* `acceptance_criteria`

La diferencia práctica es enorme: el router puede “reconstruir” el estado sin alucinar.

---

## 5) Reglas de orquestación DS (lo que yo añadiría a tu router)

### “Siempre delega” pero con dos excepciones

* **Exception 1: Clarificación de requisitos** (preguntas al usuario)
* **Exception 2: Respuesta trivial de navegación** (“dónde está el fichero”, “cómo ejecutar X”), siempre que no implique decisión técnica.

### Definition of Done por tipo

* **Dataset listo**: contract + DQ tests + pipeline + sample + runbook.
* **Modelo listo offline**: baseline + comparación + CV/backtest + reporte de errores + reproducibilidad.
* **Modelo listo prod**: todo lo anterior + serving + monitoring + rollback + CI.

### Contratos entre agentes (anti-fricción)

* DS no pide features hasta tener contract.
* MLE no implementa serving hasta tener eval protocol estable.
* DE no “optimiza” sin métricas de coste/latencia objetivo.

---

## 6) Set mínimo de ficheros (los que “deberías” crear)

En tu repo (siguiendo tu patrón actual), yo crearía:

**Agentes**

* `head-of-ds-router.md` (nuevo router)
* `data-engineer.md`
* `data-scientist.md`
* `ml-engineer.md`
* `validator.md` (ajustado a DS)

**Prompts reutilizables**

* `kickoff_problem_framing.prompt.md`
* `data_contract_and_dq.prompt.md`
* `baseline_and_eval_protocol.prompt.md`
* `train_and_package_model.prompt.md`
* `production_readiness.prompt.md`

**Instrucciones con applyTo** (si tu setup lo soporta)

* `python.instructions.md` applyTo `**/*.py`
* `tests.instructions.md` applyTo `tests/**/*.py`
* `docs.instructions.md` applyTo `**/*.md` y `**/*.qmd`
* `pipelines.instructions.md` applyTo `pipelines/**`

---

## 7) Mejoras puntuales a TU router (sin reescribirlo entero)

* Quita emojis del router (tú prefieres sin emojis; además en instrucciones conviene sobriedad).
* Cambia “Never respond directly” por:

  * “Never provide specialist content without delegation **except** trivial clarifications.”
* Añade una sección **Decision Log** (aunque sea breve).
* Cambia el umbral “>100 lines” por “multi-phase + deliverables + dependencies”; el número de líneas es un proxy malo.




