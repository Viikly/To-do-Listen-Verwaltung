<template>
  <nav class="navbar navbar-expand-lg bg-body border-bottom shadow-sm">
    <div class="container">
      <RouterLink class="navbar-brand fw-bold" to="/todos">To-do List Management</RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#mainNavigation"
        aria-controls="mainNavigation"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div id="mainNavigation" class="collapse navbar-collapse">
        <div class="navbar-nav ms-auto">
          <RouterLink class="nav-link" to="/todos">Todos</RouterLink>
          <RouterLink class="nav-link" to="/todos/new">New Todo</RouterLink>
          <RouterLink class="nav-link" to="/about">About</RouterLink>
        </div>
      </div>
    </div>
  </nav>

  <div class="container py-4">
    <header class="mb-4">
      <p class="text-uppercase text-secondary fw-semibold small mb-1">Web-Technologien I</p>
      <h1 class="display-6 fw-bold mb-0">To-do List Management</h1>
    </header>
    <RouterView />
  </div>
</template>
