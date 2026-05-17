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
const error = ref("");
const form = reactive({
  title: "",
  description: "",
  dueDate: "",
  priority: "medium",
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
    form.completed = todo.completed;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}

async function saveTodo() {
  error.value = "";

  try {
    await updateTodo(props.id, {
      title: form.title,
      description: form.description || null,
      dueDate: form.dueDate || null,
      priority: form.priority,
      completed: form.completed,
    });
    router.push("/todos");
  } catch (err) {
    error.value = err.message;
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
  <main class="panel">
    <h2>Edit Todo</h2>
    <p v-if="loading" class="message">Loading todo...</p>
    <p v-if="error" class="message error">{{ error }}</p>

    <form v-if="!loading" class="todo-form" @submit.prevent="saveTodo">
      <label>
        Title
        <input v-model.trim="form.title" type="text" maxlength="120" required>
      </label>
      <label>
        Description
        <textarea v-model.trim="form.description" rows="4"></textarea>
      </label>
      <label>
        Due date
        <input v-model="form.dueDate" type="date">
      </label>
      <label>
        Priority
        <select v-model="form.priority">
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </label>
      <label class="inline-check">
        <input v-model="form.completed" type="checkbox">
        Completed
      </label>
      <div class="form-actions">
        <button type="submit">Save</button>
        <button class="danger-button" type="button" @click="removeTodo">Delete</button>
        <RouterLink class="button secondary-button" to="/todos">Back</RouterLink>
      </div>
    </form>
  </main>
</template>
