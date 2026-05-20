const API_BASE_URL = "http://127.0.0.1:5000/api";

async function handleResponse(response) {
  if (response.status === 204) {
    return null;
  }

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.message || `Request failed with status ${response.status}.`);
  }
  return data;
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  return handleResponse(response);
}

export async function getTodos(params = {}) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value) {
      searchParams.set(key, value);
    }
  });
  const query = searchParams.toString();
  return await request(`/todos${query ? `?${query}` : ""}`);
}

export async function getTodo(id) {
  return await request(`/todos/${id}`);
}

export async function createTodo(todo) {
  return await request("/todos", {
    method: "POST",
    body: JSON.stringify(todo),
  });
}

export async function updateTodo(id, todo) {
  return await request(`/todos/${id}`, {
    method: "PUT",
    body: JSON.stringify(todo),
  });
}

export async function patchTodo(id, partialTodo) {
  return await request(`/todos/${id}`, {
    method: "PATCH",
    body: JSON.stringify(partialTodo),
  });
}

export async function deleteTodo(id) {
  return await request(`/todos/${id}`, {
    method: "DELETE",
  });
}
