import {Route, Routes} from "react-router";
import LoginPage from "@/features/auth/LoginPage.tsx";
import DashboardPage from "@/features/dashboard/DashboardPage.tsx";
import SideBarLayout from "@/layouts/SideBarLayout.tsx";
import WorkflowsPage from "@/features/workflows/WorkflowsPage.tsx";

const AppRoutes = () => {
    return (
        <Routes>
            <Route index element={<LoginPage/>}/>
            <Route path="/dashboard" element={<SideBarLayout/>}>
                <Route index element={<DashboardPage/>}/>
                <Route path="workflows" element={<WorkflowsPage/>}/>
            </Route>
        </Routes>
    );
}

export default AppRoutes;
