import { FormEvent } from "react";
import { login } from "../lib/api";
import { NextPage } from "next";

const handleLogin = (e: FormEvent) => {
  e.preventDefault();

  login("asd", "asd");
};

const LoginPage: NextPage = () => {
  return (
    <div className="flex h-screen bg-indigo-500">
      <main className="container bg-white m-auto max-w-lg rounded-3xl shadow overflow-hidden pt-6">
        <h1 className="text-4xl font-bold text-center">Login</h1>
        <form className="flex flex-col p-8 space-y-10 align-middle" onSubmit={handleLogin}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            className="text-2xl text-center text-gray-900 placeholder-gray-800 text-gray-300 border-b-2"
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            className="text-2xl text-center text-gray-900 placeholder-gray-800 text-gray-300 border-b-2"
          />

          <button name="submit" className="btn bg-indigo-500 mt-10">
            Login
          </button>
        </form>

        <div className="flex justify-evenly bg-indigo-200 p-5 w-full">
          <a href="/" className="hover:underline">
            Forget Password?
          </a>
          <a href="/signup" className="hover:underline">
            Create an account!
          </a>
        </div>
      </main>
    </div>
  );
};

export default LoginPage;
