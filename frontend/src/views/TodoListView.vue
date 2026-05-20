<script setup>
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import { deleteTodo, getTodos, patchTodo } from "../services/todoApi";

const todos = ref([]);
const loading = ref(false);
const error = ref("");
const success = ref("");
const status = ref("all");
const search = ref("");
const pendingDeleteId = ref(null);

async function loadTodos() {
  loading.value = true;
  error.value = "";
  success.value = "";

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
  error.value = "";
  success.value = "";

  try {
    await patchTodo(todo.id, { completed: !todo.completed });
    await loadTodos();
    success.value = todo.completed ? "Todo marked as open." : "Todo completed.";
  } catch (err) {
    error.value = err.message;
  }
}

async function removeTodo(todo) {
  error.value = "";
  success.value = "";
  try {
    await deleteTodo(todo.id);
    pendingDeleteId.value = null;
    await loadTodos();
    success.value = "Todo deleted.";
  } catch (err) {
    error.value = err.message;
  }
}

function changeStatus(nextStatus) {
  status.value = nextStatus;
  pendingDeleteId.value = null;
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
    <section class="card shadow-sm mb-3">
      <div class="card-body d-flex flex-column flex-lg-row gap-3 align-items-lg-center justify-content-between">
        <div class="btn-group" role="group" aria-label="Todo status filter">
          <button :class="['btn', status === 'all' ? 'btn-primary' : 'btn-outline-primary']" type="button" @click="changeStatus('all')">All</button>
          <button :class="['btn', status === 'open' ? 'btn-primary' : 'btn-outline-primary']" type="button" @click="changeStatus('open')">Open</button>
          <button :class="['btn', status === 'completed' ? 'btn-primary' : 'btn-outline-primary']" type="button" @click="changeStatus('completed')">Completed</button>
        </div>
        <form class="d-flex gap-2" @submit.prevent="loadTodos">
          <input v-model="search" class="form-control" type="search" placeholder="Search todos">
          <button class="btn btn-outline-secondary" type="submit">Search</button>
        </form>
      </div>
    </section>

    <div v-if="loading" class="alert alert-info d-flex align-items-center gap-2" role="status">
      <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
      <span>Loading todos...</span>
    </div>
    <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
    <div v-if="success" class="alert alert-success" role="status">{{ success }}</div>

    <section v-if="!loading" class="list-group shadow-sm" aria-live="polite">
      <div v-if="todos.length === 0" class="list-group-item text-secondary">No todos found.</div>

      <article v-for="todo in todos" :key="todo.id" class="list-group-item todo-row" :class="{ 'todo-row-completed': todo.completed }">
        <div class="min-width-0">
          <label class="d-flex align-items-center gap-2 mb-1">
            <input :checked="todo.completed" class="form-check-input mt-0" type="checkbox" @change="toggleCompleted(todo)">
            <span class="fw-bold text-break" :class="{ 'text-decoration-line-through text-secondary': todo.completed }">{{ todo.title }}</span>
          </label>
          <p v-if="todo.description" class="text-secondary mb-2 ps-4">{{ todo.description }}</p>
          <div class="d-flex gap-2 flex-wrap ps-4">
            <span :class="['badge', todo.priority === 'high' ? 'text-bg-danger' : todo.priority === 'low' ? 'text-bg-success' : 'text-bg-warning']">{{ priorityLabel(todo.priority) }}</span>
            <span class="badge text-bg-light border">{{ todo.dueDate ? `Due: ${todo.dueDate}` : "No due date" }}</span>
            <span :class="['badge', todo.completed ? 'text-bg-success' : 'text-bg-secondary']">{{ todo.completed ? "Completed" : "Open" }}</span>
          </div>
        </div>
        <div class="d-flex gap-2 flex-wrap">
          <RouterLink class="btn btn-outline-secondary btn-sm" :to="`/todos/${todo.id}`">Edit</RouterLink>
          <template v-if="pendingDeleteId === todo.id">
            <button class="btn btn-danger btn-sm" type="button" @click="removeTodo(todo)">Confirm delete</button>
            <button class="btn btn-outline-secondary btn-sm" type="button" @click="pendingDeleteId = null">Cancel</button>
          </template>
          <button v-else class="btn btn-outline-danger btn-sm" type="button" @click="pendingDeleteId = todo.id">Delete</button>
        </div>
      </article>
    </section>
  </main>
</template>
