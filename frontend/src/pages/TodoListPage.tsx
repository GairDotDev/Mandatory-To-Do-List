import { useState, FormEvent } from 'react';
import { useTodos } from '../hooks/useTodos';
import { Todo } from '../services/api';

export function TodoListPage() {
  const { todos, isLoading, error, createTodo, updateTodo, deleteTodo } = useTodos();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isCreating, setIsCreating] = useState(false);

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsCreating(true);
    try {
      await createTodo({ title: title.trim(), description: description.trim() });
      setTitle('');
      setDescription('');
    } catch (err) {
      // Error is handled by useTodos hook
    } finally {
      setIsCreating(false);
    }
  };

  const handleToggle = async (todo: Todo) => {
    try {
      await updateTodo(todo.id, { completed: !todo.completed });
    } catch (err) {
      // Error is handled by useTodos hook
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      try {
        await deleteTodo(id);
      } catch (err) {
        // Error is handled by useTodos hook
      }
    }
  };

  if (isLoading && todos.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-5 border-b border-gray-200">
            <h1 className="text-2xl font-bold text-gray-900">My Todos</h1>
          </div>

          {/* Create Todo Form */}
          <div className="px-6 py-5 border-b border-gray-200">
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                  Title
                </label>
                <input
                  type="text"
                  id="title"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  placeholder="Enter todo title"
                />
              </div>
              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                  Description (optional)
                </label>
                <textarea
                  id="description"
                  rows={3}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  placeholder="Enter todo description"
                />
              </div>
              <button
                type="submit"
                disabled={isCreating || !title.trim()}
                className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {isCreating ? 'Adding...' : 'Add Todo'}
              </button>
            </form>
          </div>

          {/* Error Display */}
          {error && (
            <div className="px-6 py-4 bg-red-50 border-b border-red-200">
              <div className="text-sm text-red-800">{error}</div>
            </div>
          )}

          {/* Todo List */}
          <div className="divide-y divide-gray-200">
            {todos.length === 0 ? (
              <div className="px-6 py-12 text-center text-gray-500">
                No todos yet. Create your first todo above!
              </div>
            ) : (
              todos.map((todo) => (
                <div key={todo.id} className="px-6 py-4 hover:bg-gray-50">
                  <div className="flex items-start">
                    <div className="flex items-center h-5">
                      <input
                        type="checkbox"
                        checked={todo.completed}
                        onChange={() => handleToggle(todo)}
                        className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                      />
                    </div>
                    <div className="ml-3 flex-1">
                      <h3
                        className={`text-lg font-medium ${
                          todo.completed ? 'line-through text-gray-400' : 'text-gray-900'
                        }`}
                      >
                        {todo.title}
                      </h3>
                      {todo.description && (
                        <p
                          className={`mt-1 text-sm ${
                            todo.completed ? 'text-gray-400' : 'text-gray-500'
                          }`}
                        >
                          {todo.description}
                        </p>
                      )}
                      <p className="mt-1 text-xs text-gray-400">
                        Created: {new Date(todo.created_at).toLocaleString()}
                      </p>
                    </div>
                    <button
                      onClick={() => handleDelete(todo.id)}
                      className="ml-4 text-red-600 hover:text-red-800 text-sm font-medium"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

