import { createRouter, createWebHistory } from "vue-router";
import TodoListView from "../views/TodoListView.vue";
import TodoCreateView from "../views/TodoCreateView.vue";
import TodoDetailView from "../views/TodoDetailView.vue";
import AboutView from "../views/AboutView.vue";

const routes = [
  { path: "/", redirect: "/todos" },
  { path: "/todos", name: "todos", component: TodoListView },
  { path: "/todos/new", name: "todo-create", component: TodoCreateView },
  { path: "/todos/:id", name: "todo-detail", component: TodoDetailView, props: true },
  { path: "/about", name: "about", component: AboutView },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
