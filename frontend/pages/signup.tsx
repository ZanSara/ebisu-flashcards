import { NextPage } from "next";

const SignupPage: NextPage = () => (
  <div className="flex h-screen bg-indigo-500">
    <main className="container bg-white m-auto max-w-lg rounded-3xl shadow overflow-hidden">
      <form className="flex flex-col p-8">
        <h1 className="text-4xl font-bold text-center">Sign up!</h1>

        <input type="text" name="username" placeholder="Username" className="txt" />
        <input type="email" name="email" placeholder="E-Mail" className="txt" />
        <input type="password" name="password" placeholder="Password" className="txt" />

        <button name="submit" className="btn bg-indigo-500 mt-10">
          Sign me up!
        </button>
      </form>

      <div className="flex justify-evenly bg-indigo-200 p-5 w-full">
        <a href="/privacy" className="hover:underline">
          Privacy Policy
        </a>
      </div>
    </main>
  </div>
);

export default SignupPage;
