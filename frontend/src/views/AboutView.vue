<template>
  <main class="panel">
    <h2>About this project</h2>
    <p>
      This project is an API-first to-do list application for Web-Technologien I.
      The OpenAPI file describes the REST API before the frontend uses it.
    </p>
    <div class="architecture-grid">
      <section>
        <h3>Presentation layer</h3>
        <p>Vue.js SPA with Vue Router.</p>
      </section>
      <section>
        <h3>Logic layer</h3>
        <p>Flask backend with routes and service logic.</p>
      </section>
      <section>
        <h3>Data layer</h3>
        <p>SQLite persistence with parameterized SQL queries.</p>
      </section>
    </div>
  </main>
</template>
