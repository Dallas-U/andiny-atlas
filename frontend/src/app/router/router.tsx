import {
    Outlet,
    createRootRouteWithContext,
    createRoute,
    createRouter,
    redirect,
} from "@tanstack/react-router";

import AuthLayout from "../../layouts/AuthLayout";
import DashboardPage from "../../pages/DashboardPage";
import LoginPage from "../../pages/LoginPage";
import InvestigationsPage from "../../pages/InvestigationsPage";
import ReportsPage from "../../features/reports/pages/ReportsPage";
import NewInvestigationPage from "../../pages/NewInvestigationPage";
import AnalyticsPage from "../../features/analytics/pages/AnalyticsPage";
import InvestigationDetailsPage from "../../pages/InvestigationDetailsPage";
import ExportCenterPage from "../../features/exports/pages/ExportCenterPage";
import ExecutiveDashboardPage from "../../features/enterpriseAnalytics/pages/ExecutiveDashboardPage";
import CustomerAdministrationPage from "../../features/customerAdministration/pages/CustomerAdministrationPage";
import OrganizationAdministrationPage from "../../features/organizations/pages/OrganizationAdministrationPage";
import UserAdministrationPage from "../../features/administration/pages/UserAdministrationPage";

interface RouterAuthContext {
    isAuthenticated: boolean;
}

interface RouterContext {
    auth: RouterAuthContext;
}

const rootRoute = createRootRouteWithContext<RouterContext>()({
    component: RootComponent,
});

function RootComponent() {
    return <Outlet />;
}

const authLayoutRoute = createRoute({
    getParentRoute: () => rootRoute,
    id: "auth",
    component: AuthLayoutRoute,
});

function AuthLayoutRoute() {
    return (
        <AuthLayout>
            <Outlet />
        </AuthLayout>
    );
}

const loginRoute = createRoute({
    getParentRoute: () => authLayoutRoute,
    path: "/",
    beforeLoad: ({ context }) => {
        if (context.auth.isAuthenticated) {
            throw redirect({
                to: "/dashboard",
                replace: true,
            });
        }
    },
    component: LoginPage,
});

const dashboardRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/dashboard",
    beforeLoad: ({ context }) => {
        if (!context.auth.isAuthenticated) {
            throw redirect({
                to: "/",
                replace: true,
            });
        }
    },
    component: DashboardPage,
});

const newInvestigationRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/dashboard/new-investigation",
    beforeLoad: ({ context }) => {
        if (!context.auth.isAuthenticated) {
            throw redirect({
                to: "/",
                replace: true,
            });
        }
    },
    component: NewInvestigationPage,
});

const investigationsRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/dashboard/investigations",
    beforeLoad: ({ context }) => {
        if (!context.auth.isAuthenticated) {
            throw redirect({
                to: "/",
                replace: true,
            });
        }
    },
    component: InvestigationsPage,
});

const investigationDetailsRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/dashboard/investigations/$caseId",
    beforeLoad: ({ context }) => {
        if (!context.auth.isAuthenticated) {
            throw redirect({
                to: "/",
                replace: true,
            });
        }
    },
    component: InvestigationDetailsPage,
});

const reportsRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/dashboard/reports",
    beforeLoad: ({ context }) => {
        if (!context.auth.isAuthenticated) {
            throw redirect({
                to: "/",
                replace: true,
            });
        }
    },
    component: ReportsPage,
});

const analyticsRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/dashboard/analytics",
    beforeLoad: ({ context }) => {
        if (!context.auth.isAuthenticated) {
            throw redirect({
                to: "/",
                replace: true,
            });
        }
    },
    component: AnalyticsPage,
});

const organizationsRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/dashboard/organizations",
    beforeLoad: ({ context }) => {
        if (!context.auth.isAuthenticated) {
            throw redirect({
                to: "/",
                replace: true,
            });
        }
    },
    component: ExecutiveDashboardPage,
});

const exportsRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/dashboard/exports",
    beforeLoad: ({ context }) => {
        if (!context.auth.isAuthenticated) {
            throw redirect({
                to: "/",
                replace: true,
            });
        }
    },
    component: ExportCenterPage,
});

const userAdministrationRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/dashboard/administration/users",
    beforeLoad: ({ context }) => {
        if (!context.auth.isAuthenticated) {
            throw redirect({
                to: "/",
                replace: true,
            });
        }
    },
    component: UserAdministrationPage,
});

const customerAdministrationRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/dashboard/administration/customer",
    beforeLoad: ({ context }) => {
        if (!context.auth.isAuthenticated) {
            throw redirect({
                to: "/",
                replace: true,
            });
        }
    },
    component: CustomerAdministrationPage,
});

const organizationAdministrationRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/dashboard/administration/organizations",
    beforeLoad: ({ context }) => {
        if (!context.auth.isAuthenticated) {
            throw redirect({
                to: "/",
                replace: true,
            });
        }
    },
    component: OrganizationAdministrationPage,
});

const routeTree = rootRoute.addChildren([
    authLayoutRoute.addChildren([loginRoute]),
    dashboardRoute,
    newInvestigationRoute,
    investigationsRoute,
    investigationDetailsRoute,
    reportsRoute,
    analyticsRoute,
    organizationsRoute,
    exportsRoute,
    userAdministrationRoute,
    customerAdministrationRoute,
    organizationAdministrationRoute,
]);

export const router = createRouter({
    routeTree,
    context: {
        auth: undefined!,
    },
});

declare module "@tanstack/react-router" {
    interface Register {
        router: typeof router;
    }
}