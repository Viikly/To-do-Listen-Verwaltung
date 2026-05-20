<template>
  <main class="card shadow-sm">
    <div class="card-body">
      <h2 class="h4 card-title mb-3">About this project</h2>
      <p class="card-text">
        This project is an API-first to-do list application for Web-Technologien I.
        The OpenAPI file describes the REST API before the frontend uses it.
      </p>
      <div class="row g-3">
        <section class="col-md-4">
          <div class="border rounded p-3 h-100">
            <span class="badge text-bg-primary mb-2">Presentation</span>
            <h3 class="h6">Vue.js SPA</h3>
            <p class="mb-0 text-secondary">Vue Router, Bootstrap UI and fetch API calls.</p>
          </div>
        </section>
        <section class="col-md-4">
          <div class="border rounded p-3 h-100">
            <span class="badge text-bg-secondary mb-2">Logic</span>
            <h3 class="h6">Flask backend</h3>
            <p class="mb-0 text-secondary">Routes, validation and todo service logic.</p>
          </div>
        </section>
        <section class="col-md-4">
          <div class="border rounded p-3 h-100">
            <span class="badge text-bg-success mb-2">Data</span>
            <h3 class="h6">SQLite</h3>
            <p class="mb-0 text-secondary">Persistent storage with parameterized SQL queries.</p>
          </div>
        </section>
      </div>
    </div>
  </main>
</template>
