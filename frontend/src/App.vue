<template>
  <div class="app-shell">
    <header class="page-header">
      <div>
        <p class="eyebrow">Web-Technologien I</p>
        <h1>To-do List Management</h1>
      </div>
      <nav class="main-nav" aria-label="Main navigation">
        <RouterLink to="/todos">Todos</RouterLink>
        <RouterLink to="/todos/new">New Todo</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </header>

    <RouterView />
  </div>
</template>
