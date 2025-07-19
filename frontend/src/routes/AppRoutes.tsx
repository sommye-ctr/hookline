import {Route, Routes} from "react-router";
import LoginPage from "@/pages/LoginPage.tsx";
import DashboardPage from "@/pages/DashboardPage.tsx";
import SideBarLayout from "@/components/SideBarLayout.tsx";
import WorkflowsPage from "@/pages/WorkflowsPage.tsx";

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
