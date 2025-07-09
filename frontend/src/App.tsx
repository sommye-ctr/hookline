import {LoginForm} from "@/components/login-form.tsx";

function App() {
    return (
        <div className="flex flex-col min-h-svh w-full items-center justify-center p-6 md:p-10">
            <h1 className="mb-2 text-primary">Hookline</h1>
            <h3 className="mb-6">Sign in to your account</h3>
            <div className="w-full max-w-sm">
                <LoginForm/>
            </div>
        </div>
    )
}

export default App
