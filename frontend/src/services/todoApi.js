const API_BASE_URL = "http://localhost:5000/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (response.status === 204) {
    return null;
  }

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.message || "API request failed.");
  }
  return data;
}

export function getTodos(params = {}) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value) {
      searchParams.set(key, value);
    }
  });
  const query = searchParams.toString();
  return request(`/todos${query ? `?${query}` : ""}`);
}

export function getTodo(id) {
  return request(`/todos/${id}`);
}

export function createTodo(todo) {
  return request("/todos", {
    method: "POST",
    body: JSON.stringify(todo),
  });
}

export function updateTodo(id, todo) {
  return request(`/todos/${id}`, {
    method: "PUT",
    body: JSON.stringify(todo),
  });
}

export function patchTodo(id, partialTodo) {
  return request(`/todos/${id}`, {
    method: "PATCH",
    body: JSON.stringify(partialTodo),
  });
}

export function deleteTodo(id) {
  return request(`/todos/${id}`, {
    method: "DELETE",
  });
}
