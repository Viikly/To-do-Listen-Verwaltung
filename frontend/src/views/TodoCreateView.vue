<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { createTodo } from "../services/todoApi";

const router = useRouter();
const error = ref("");
const saving = ref(false);
const form = reactive({
  title: "",
  description: "",
  dueDate: "",
  priority: "medium",
  status: "todo",
});

async function submitTodo() {
  error.value = "";
  saving.value = true;

  try {
    const created = await createTodo({
      title: form.title,
      description: form.description || null,
      dueDate: form.dueDate || null,
      priority: form.priority,
      status: form.status,
    });
    router.push(`/todos/${created.id}`);
  } catch (err) {
    error.value = err.message;
  } finally {
    saving.value = false;
  }
}
</script>

<template>
  <main class="card shadow-sm">
    <div class="card-body">
      <h2 class="h4 card-title mb-3">Create Todo</h2>
      <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>

      <form class="row g-3" @submit.prevent="submitTodo">
        <div class="col-12">
          <label class="form-label" for="todo-title">Title</label>
          <input id="todo-title" v-model.trim="form.title" class="form-control" type="text" maxlength="120" required>
        </div>
        <div class="col-12">
          <label class="form-label" for="todo-description">Description</label>
          <textarea id="todo-description" v-model.trim="form.description" class="form-control" rows="4"></textarea>
        </div>
        <div class="col-md-6">
          <label class="form-label" for="todo-due-date">Due date</label>
          <input id="todo-due-date" v-model="form.dueDate" class="form-control" type="date">
        </div>
        <div class="col-md-6">
          <label class="form-label" for="todo-priority">Priority</label>
          <select id="todo-priority" v-model="form.priority" class="form-select">
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
        <div class="col-md-6">
          <label class="form-label" for="todo-status">Status</label>
          <select id="todo-status" v-model="form.status" class="form-select">
            <option value="todo">To-do</option>
            <option value="in_progress">In progress</option>
            <option value="done">Done</option>
          </select>
        </div>
        <div class="col-12 d-flex gap-2">
          <button class="btn btn-primary" type="submit" :disabled="saving">
            <span v-if="saving" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
            {{ saving ? "Creating..." : "Create" }}
          </button>
          <RouterLink class="btn btn-outline-secondary" to="/todos">Cancel</RouterLink>
        </div>
      </form>
    </div>
  </main>
</template>
