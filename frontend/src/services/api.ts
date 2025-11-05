import axios, { AxiosInstance, AxiosError } from 'axios';
import API_BASE_URL from '../config/api';

export interface Todo {
  id: number;
  user_id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTodoRequest {
  title: string;
  description?: string;
}

export interface UpdateTodoRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface User {
  id: number;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to requests if available
    const token = localStorage.getItem('token');
    if (token) {
      this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }

  setAuthToken(token: string | null) {
    if (token) {
      this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      localStorage.setItem('token', token);
    } else {
      delete this.client.defaults.headers.common['Authorization'];
      localStorage.removeItem('token');
    }
  }

  // Auth endpoints
  async register(data: RegisterRequest): Promise<User> {
    const response = await this.client.post<User>('/api/v1/auth/register', data);
    return response.data;
  }

  async login(data: LoginRequest): Promise<LoginResponse> {
    const response = await this.client.post<LoginResponse>('/api/v1/auth/login', data);
    this.setAuthToken(response.data.access_token);
    return response.data;
  }

  logout() {
    this.setAuthToken(null);
  }

  // Todo endpoints
  async getTodos(): Promise<Todo[]> {
    const response = await this.client.get<Todo[]>('/api/v1/todos');
    return response.data;
  }

  async getTodo(id: number): Promise<Todo> {
    const response = await this.client.get<Todo>(`/api/v1/todos/${id}`);
    return response.data;
  }

  async createTodo(data: CreateTodoRequest): Promise<Todo> {
    const response = await this.client.post<Todo>('/api/v1/todos', data);
    return response.data;
  }

  async updateTodo(id: number, data: UpdateTodoRequest): Promise<Todo> {
    const response = await this.client.put<Todo>(`/api/v1/todos/${id}`, data);
    return response.data;
  }

  async deleteTodo(id: number): Promise<void> {
    await this.client.delete(`/api/v1/todos/${id}`);
  }

}

// Helper function to handle errors
export function handleApiError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ error?: string }>;
    if (axiosError.response) {
      return axiosError.response.data?.error || axiosError.message;
    }
    return axiosError.message;
  }
  return 'An unexpected error occurred';
}

export default new ApiClient();

