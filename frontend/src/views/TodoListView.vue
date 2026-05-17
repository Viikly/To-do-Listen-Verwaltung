<script setup>
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import { deleteTodo, getTodos, patchTodo } from "../services/todoApi";

const todos = ref([]);
const loading = ref(false);
const error = ref("");
const status = ref("all");
const search = ref("");

async function loadTodos() {
  loading.value = true;
  error.value = "";

  try {
    todos.value = await getTodos({
      status: status.value,
      q: search.value.trim(),
    });
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}

async function toggleCompleted(todo) {
  try {
    await patchTodo(todo.id, { completed: !todo.completed });
    await loadTodos();
  } catch (err) {
    error.value = err.message;
  }
}

async function removeTodo(todo) {
  if (!window.confirm(`Delete "${todo.title}"?`)) {
    return;
  }

  try {
    await deleteTodo(todo.id);
    await loadTodos();
  } catch (err) {
    error.value = err.message;
  }
}

function changeStatus(nextStatus) {
  status.value = nextStatus;
  loadTodos();
}

function priorityLabel(priority) {
  return {
    low: "Low",
    medium: "Medium",
    high: "High",
  }[priority] || "Medium";
}

onMounted(loadTodos);
</script>

<template>
  <main>
    <section class="toolbar">
      <div class="filter-group">
        <button :class="{ active: status === 'all' }" type="button" @click="changeStatus('all')">All</button>
        <button :class="{ active: status === 'open' }" type="button" @click="changeStatus('open')">Open</button>
        <button :class="{ active: status === 'completed' }" type="button" @click="changeStatus('completed')">Completed</button>
      </div>
      <form class="search-form" @submit.prevent="loadTodos">
        <input v-model="search" type="search" placeholder="Search todos">
        <button type="submit">Search</button>
      </form>
    </section>

    <p v-if="loading" class="message">Loading todos...</p>
    <p v-if="error" class="message error">{{ error }}</p>

    <section v-if="!loading" class="todo-list" aria-live="polite">
      <p v-if="todos.length === 0" class="message">No todos found.</p>

      <article v-for="todo in todos" :key="todo.id" class="todo-item" :class="{ completed: todo.completed }">
        <div class="todo-main">
          <label class="checkbox-row">
            <input :checked="todo.completed" type="checkbox" @change="toggleCompleted(todo)">
            <span class="todo-title">{{ todo.title }}</span>
          </label>
          <p v-if="todo.description" class="todo-description">{{ todo.description }}</p>
          <div class="todo-meta">
            <span :class="['priority', todo.priority || 'medium']">{{ priorityLabel(todo.priority) }}</span>
            <span>{{ todo.dueDate ? `Due: ${todo.dueDate}` : "No due date" }}</span>
          </div>
        </div>
        <div class="todo-actions">
          <RouterLink class="button secondary-button" :to="`/todos/${todo.id}`">Edit</RouterLink>
          <button class="danger-button" type="button" @click="removeTodo(todo)">Delete</button>
        </div>
      </article>
    </section>
  </main>
</template>
