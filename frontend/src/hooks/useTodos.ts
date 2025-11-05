import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import apiClient, { Todo, CreateTodoRequest, UpdateTodoRequest, handleApiError } from '../services/api';

export function useTodos() {
  const { isAuthenticated } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTodos = async () => {
    if (!isAuthenticated) return;

    setIsLoading(true);
    setError(null);
    try {
      const data = await apiClient.getTodos();
      setTodos(data);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTodos();
  }, [isAuthenticated]);

  const createTodo = async (data: CreateTodoRequest) => {
    try {
      const newTodo = await apiClient.createTodo(data);
      setTodos((prev) => [newTodo, ...prev]);
      return newTodo;
    } catch (err) {
      const errorMessage = handleApiError(err);
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  const updateTodo = async (id: number, data: UpdateTodoRequest) => {
    try {
      const updatedTodo = await apiClient.updateTodo(id, data);
      setTodos((prev) =>
        prev.map((todo) => (todo.id === id ? updatedTodo : todo))
      );
      return updatedTodo;
    } catch (err) {
      const errorMessage = handleApiError(err);
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  const deleteTodo = async (id: number) => {
    try {
      await apiClient.deleteTodo(id);
      setTodos((prev) => prev.filter((todo) => todo.id !== id));
    } catch (err) {
      const errorMessage = handleApiError(err);
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  return {
    todos,
    isLoading,
    error,
    fetchTodos,
    createTodo,
    updateTodo,
    deleteTodo,
  };
}

