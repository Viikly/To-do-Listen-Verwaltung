<script setup>
import { onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { deleteTodo, getTodo, updateTodo } from "../services/todoApi";

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const router = useRouter();
const loading = ref(false);
const saving = ref(false);
const error = ref("");
const form = reactive({
  title: "",
  description: "",
  dueDate: "",
  priority: "medium",
  status: "todo",
  archived: false,
  completed: false,
});

async function loadTodo() {
  loading.value = true;
  error.value = "";

  try {
    const todo = await getTodo(props.id);
    form.title = todo.title;
    form.description = todo.description || "";
    form.dueDate = todo.dueDate || "";
    form.priority = todo.priority || "medium";
    form.status = todo.status || (todo.completed ? "done" : "todo");
    form.archived = todo.archived;
    form.completed = todo.completed;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}

async function saveTodo() {
  error.value = "";
  saving.value = true;

  try {
    await updateTodo(props.id, {
      title: form.title,
      description: form.description || null,
      dueDate: form.dueDate || null,
      priority: form.priority,
      status: form.status,
      archived: form.archived,
    });
    router.push("/todos");
  } catch (err) {
    error.value = err.message;
  } finally {
    saving.value = false;
  }
}

async function removeTodo() {
  if (!window.confirm("Delete this todo?")) {
    return;
  }

  try {
    await deleteTodo(props.id);
    router.push("/todos");
  } catch (err) {
    error.value = err.message;
  }
}

onMounted(loadTodo);
</script>

<template>
  <main class="card shadow-sm">
    <div class="card-body">
      <h2 class="h4 card-title mb-3">Edit Todo</h2>
      <div v-if="loading" class="alert alert-info d-flex align-items-center gap-2" role="status">
        <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
        <span>Loading todo...</span>
      </div>
      <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>

      <form v-if="!loading" class="row g-3" @submit.prevent="saveTodo">
        <div class="col-12">
          <label class="form-label" for="edit-title">Title</label>
          <input id="edit-title" v-model.trim="form.title" class="form-control" type="text" maxlength="120" required>
        </div>
        <div class="col-12">
          <label class="form-label" for="edit-description">Description</label>
          <textarea id="edit-description" v-model.trim="form.description" class="form-control" rows="4"></textarea>
        </div>
        <div class="col-md-6">
          <label class="form-label" for="edit-due-date">Due date</label>
          <input id="edit-due-date" v-model="form.dueDate" class="form-control" type="date">
        </div>
        <div class="col-md-6">
          <label class="form-label" for="edit-priority">Priority</label>
          <select id="edit-priority" v-model="form.priority" class="form-select">
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
        <div class="col-md-6">
          <label class="form-label" for="edit-status">Status</label>
          <select id="edit-status" v-model="form.status" class="form-select">
            <option value="todo">To-do</option>
            <option value="in_progress">In progress</option>
            <option value="done">Done</option>
          </select>
        </div>
        <div class="col-12 d-flex gap-4 flex-wrap">
          <div class="form-check">
            <input id="edit-archived" v-model="form.archived" class="form-check-input" type="checkbox">
            <label class="form-check-label" for="edit-archived">Archived</label>
          </div>
        </div>
        <div class="col-12 d-flex gap-2 flex-wrap">
          <button class="btn btn-primary" type="submit" :disabled="saving">
            <span v-if="saving" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
            {{ saving ? "Saving..." : "Save" }}
          </button>
          <button class="btn btn-outline-danger" type="button" @click="removeTodo">Delete</button>
          <RouterLink class="btn btn-outline-secondary" to="/todos">Back</RouterLink>
        </div>
      </form>
    </div>
  </main>
</template>
