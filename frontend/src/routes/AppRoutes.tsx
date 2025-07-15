import {Routes, Route} from "react-router";
import LoginPage from "@/pages/LoginPage.tsx";
import DashboardPage from "@/pages/DashboardPage.tsx";

const AppRoutes = () => {
    return (
        <Routes>
            <Route index element={<LoginPage/>}/>
            <Route path="/dashboard" element={<DashboardPage/>}/>
        </Routes>
    );
}

export default AppRoutes;
