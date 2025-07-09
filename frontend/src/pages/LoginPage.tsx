import {LoginForm} from "@/components/login-form.tsx";
import {useState} from "react";


const LoginPage = () => {
    const [isLogin, setIsLogin] = useState(true);

    const onSecondaryActionClicked = () => setIsLogin(!isLogin);

    return (
        <div className="flex flex-col min-h-svh w-full items-center justify-center p-6 md:p-10">
            <h1 className="mb-2 text-primary">Hookline</h1>
            <h3 className="mb-6">
                {isLogin ? "Sign in to your account" : "Create a new account"}
            </h3>
            <div className="w-full max-w-sm">
                <LoginForm login={isLogin} onSecondaryActionClicked={onSecondaryActionClicked}/>
            </div>
        </div>
    );
}

export default LoginPage;
