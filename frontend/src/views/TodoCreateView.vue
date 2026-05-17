<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { createTodo } from "../services/todoApi";

const router = useRouter();
const error = ref("");
const form = reactive({
  title: "",
  description: "",
  dueDate: "",
  priority: "medium",
});

async function submitTodo() {
  error.value = "";

  try {
    const created = await createTodo({
      title: form.title,
      description: form.description || null,
      dueDate: form.dueDate || null,
      priority: form.priority,
    });
    router.push(`/todos/${created.id}`);
  } catch (err) {
    error.value = err.message;
  }
}
</script>

<template>
  <main class="panel">
    <h2>Create Todo</h2>
    <p v-if="error" class="message error">{{ error }}</p>

    <form class="todo-form" @submit.prevent="submitTodo">
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
      <div class="form-actions">
        <button type="submit">Create</button>
        <RouterLink class="button secondary-button" to="/todos">Cancel</RouterLink>
      </div>
    </form>
  </main>
</template>
