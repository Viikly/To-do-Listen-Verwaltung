<script setup>
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import { deleteTodo, getTodoStats, getTodos, patchTodo } from "../services/todoApi";

const todos = ref([]);
const stats = ref(null);
const loading = ref(false);
const error = ref("");
const success = ref("");
const status = ref("all");
const archived = ref("false");
const dueDate = ref("");
const dueBefore = ref("");
const dueAfter = ref("");
const search = ref("");
const pendingDeleteId = ref(null);

async function loadTodos() {
  loading.value = true;
  error.value = "";
  success.value = "";

  try {
    todos.value = await getTodos({
      status: status.value,
      archived: archived.value,
      dueDate: dueDate.value,
      dueBefore: dueBefore.value,
      dueAfter: dueAfter.value,
      q: search.value.trim(),
    });
    stats.value = await getTodoStats();
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

async function archiveTodo(todo) {
  error.value = "";
  success.value = "";

  try {
    await patchTodo(todo.id, { archived: !todo.archived });
    pendingDeleteId.value = null;
    await loadTodos();
    success.value = todo.archived ? "Todo restored from archive." : "Todo archived.";
  } catch (err) {
    error.value = err.message;
  }
}

function priorityLabel(priority) {
  return {
    low: "Low",
    medium: "Medium",
    high: "High",
  }[priority] || "Medium";
}

function statusLabel(todoStatus) {
  return {
    todo: "To-do",
    in_progress: "In progress",
    done: "Done",
  }[todoStatus] || "To-do";
}

function statusBadgeClass(todoStatus) {
  return {
    todo: "text-bg-secondary",
    in_progress: "text-bg-primary",
    done: "text-bg-success",
  }[todoStatus] || "text-bg-secondary";
}

onMounted(loadTodos);
</script>

<template>
  <main>
    <section v-if="stats" class="row g-3 mb-3">
      <div class="col-6 col-lg-3">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <div class="text-secondary small">Active</div>
            <div class="fs-3 fw-bold">{{ stats.active }}</div>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <div class="text-secondary small">In progress</div>
            <div class="fs-3 fw-bold">{{ stats.inProgress }}</div>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <div class="text-secondary small">Done</div>
            <div class="fs-3 fw-bold">{{ stats.done }}</div>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <div class="text-secondary small">Archived / Overdue</div>
            <div class="fs-3 fw-bold">{{ stats.archived }} / {{ stats.overdue }}</div>
          </div>
        </div>
      </div>
    </section>

    <section class="card shadow-sm mb-3">
      <div class="card-body d-grid gap-3">
        <div class="d-flex flex-column flex-lg-row gap-3 align-items-lg-center justify-content-between">
          <div class="btn-group flex-wrap" role="group" aria-label="Todo status filter">
          <button :class="['btn', status === 'all' ? 'btn-primary' : 'btn-outline-primary']" type="button" @click="changeStatus('all')">All</button>
          <button :class="['btn', status === 'todo' ? 'btn-primary' : 'btn-outline-primary']" type="button" @click="changeStatus('todo')">To-do</button>
          <button :class="['btn', status === 'in_progress' ? 'btn-primary' : 'btn-outline-primary']" type="button" @click="changeStatus('in_progress')">In progress</button>
          <button :class="['btn', status === 'done' ? 'btn-primary' : 'btn-outline-primary']" type="button" @click="changeStatus('done')">Done</button>
          </div>
          <form class="d-flex gap-2" @submit.prevent="loadTodos">
            <input v-model="search" class="form-control" type="search" placeholder="Search todos">
            <button class="btn btn-outline-secondary" type="submit">Search</button>
          </form>
        </div>
        <div class="row g-2">
          <div class="col-md-3">
            <label class="form-label small" for="archive-filter">Archive</label>
            <select id="archive-filter" v-model="archived" class="form-select" @change="loadTodos">
              <option value="false">Active todos</option>
              <option value="true">Archived todos</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label small" for="due-date-filter">Due date</label>
            <input id="due-date-filter" v-model="dueDate" class="form-control" type="date" @change="loadTodos">
          </div>
          <div class="col-md-3">
            <label class="form-label small" for="due-before-filter">Due before</label>
            <input id="due-before-filter" v-model="dueBefore" class="form-control" type="date" @change="loadTodos">
          </div>
          <div class="col-md-3">
            <label class="form-label small" for="due-after-filter">Due after</label>
            <input id="due-after-filter" v-model="dueAfter" class="form-control" type="date" @change="loadTodos">
          </div>
        </div>
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
            <span :class="['badge', statusBadgeClass(todo.status)]">{{ statusLabel(todo.status) }}</span>
            <span v-if="todo.archived" class="badge text-bg-dark">Archived</span>
          </div>
        </div>
        <div class="d-flex gap-2 flex-wrap">
          <RouterLink class="btn btn-outline-secondary btn-sm" :to="`/todos/${todo.id}`">Edit</RouterLink>
          <button class="btn btn-outline-primary btn-sm" type="button" @click="archiveTodo(todo)">
            {{ todo.archived ? "Restore" : "Archive" }}
          </button>
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
