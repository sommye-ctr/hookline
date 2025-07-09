import {Routes, Route} from "react-router";
import LoginPage from "@/pages/LoginPage.tsx";

const AppRoutes = () => {
    return (
        <Routes>
            <Route index element={<LoginPage/>}/>
        </Routes>
    );
}

export default AppRoutes;
