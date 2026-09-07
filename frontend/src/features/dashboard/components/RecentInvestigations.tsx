import { useEffect, useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import {
    ArrowUpRight,
    FolderOpen,
} from "lucide-react";
import { useTranslation } from "react-i18next";

import Card from "../../../shared/components/Card";
import EmptyState from "../../../shared/components/EmptyState";
import LoadingSkeleton from "../../../shared/components/LoadingSkeleton";
import StatusBadge from "../../../shared/components/StatusBadge";

import {
    formatExactDate,
    formatRelativeDate,
} from "../../../shared/utils/date";

import { getMyCases } from "../../investigation/api/investigation.api";

import type {
    CaseResponse,
} from "../../investigation/types/investigation.types";


function RecentInvestigations() {
    const navigate = useNavigate();
    const { t } = useTranslation();

    const [investigations, setInvestigations] =
        useState<CaseResponse[]>([]);

    const [isLoading, setIsLoading] =
        useState(true);

    const [errorMessage, setErrorMessage] =
        useState<string | null>(null);


    useEffect(() => {
        async function loadRecentInvestigations(): Promise<void> {
            try {
                setIsLoading(true);
                setErrorMessage(null);

                const response = await getMyCases({
                    page: 1,
                    page_size: 5,
                    sort_by: "timestamp",
                    sort_order: "desc",
                });

                setInvestigations(response.items);
            } catch (error) {
                console.error(
                    "Failed to load recent investigations:",
                    error,
                );

                setErrorMessage(
                    "dashboard.recentInvestigations.loadError",
                );
            } finally {
                setIsLoading(false);
            }
        }

        void loadRecentInvestigations();
    }, []);


    function openInvestigation(
        caseId: string,
    ): void {
        void navigate({
            to: "/dashboard/investigations/$caseId",
            params: {
                caseId,
            },
        });
    }


    return (
        <section className="mt-10">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
                <div>
                    <h2 className="text-xl font-semibold text-white">
                        {t(
                            "dashboard.recentInvestigations.title",
                        )}
                    </h2>

                    <p className="mt-1 text-sm text-slate-400">
                        {t(
                            "dashboard.recentInvestigations.subtitle",
                        )}
                    </p>
                </div>

                <button
                    type="button"
                    onClick={() => {
                        void navigate({
                            to: "/dashboard/investigations",
                        });
                    }}
                    className="inline-flex items-center gap-2 text-sm font-medium text-slate-400 transition hover:text-white"
                >
                    {t(
                        "dashboard.recentInvestigations.viewAll",
                    )}

                    <ArrowUpRight className="h-4 w-4" />
                </button>
            </div>


            {isLoading && (
                <Card className="mt-4">
                    <div className="space-y-5">
                        {Array.from({
                            length: 3,
                        }).map((_, index) => (
                            <div
                                key={index}
                                className="space-y-3 border-b border-slate-800 pb-5 last:border-b-0 last:pb-0"
                            >
                                <div className="flex items-center justify-between gap-4">
                                    <LoadingSkeleton className="h-5 w-40" />

                                    <LoadingSkeleton className="h-6 w-24" />
                                </div>

                                <LoadingSkeleton className="h-4 w-32" />

                                <LoadingSkeleton className="h-4 w-3/4" />
                            </div>
                        ))}
                    </div>
                </Card>
            )}


            {!isLoading && errorMessage && (
                <Card className="mt-4 border-red-900">
                    <p className="text-red-400">
                        {t(errorMessage)}
                    </p>
                </Card>
            )}


            {!isLoading &&
                !errorMessage &&
                investigations.length === 0 && (
                    <div className="mt-4">
                        <EmptyState
                            title={t(
                                "dashboard.recentInvestigations.emptyTitle",
                            )}
                            description={t(
                                "dashboard.recentInvestigations.emptyDescription",
                            )}
                            icon={
                                <FolderOpen className="h-10 w-10" />
                            }
                        />
                    </div>
                )}


            {!isLoading &&
                !errorMessage &&
                investigations.length > 0 && (
                    <Card className="mt-4 p-0">
                        <div className="divide-y divide-slate-800">
                            {investigations.map(
                                (investigation) => (
                                    <button
                                        key={
                                            investigation.case_id
                                        }
                                        type="button"
                                        onClick={() => {
                                            openInvestigation(
                                                investigation.case_id,
                                            );
                                        }}
                                        className="w-full px-6 py-5 text-left transition hover:bg-slate-800/60"
                                    >
                                        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                                            <div className="min-w-0">
                                                <div className="flex flex-wrap items-center gap-3">
                                                    <h3 className="font-semibold text-white">
                                                        {
                                                            investigation.customer_name
                                                        }
                                                    </h3>

                                                    <StatusBadge
                                                        status={
                                                            investigation
                                                                .result
                                                                .status
                                                        }
                                                    />
                                                </div>

                                                <p className="mt-2 text-sm text-slate-400">
                                                    {
                                                        investigation.phone_number
                                                    }
                                                </p>

                                                <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-500">
                                                    {
                                                        investigation
                                                            .result
                                                            .reason
                                                    }
                                                </p>

                                                <p className="mt-3 truncate text-xs text-slate-600">
                                                    {t(
                                                        "dashboard.recentInvestigations.case",
                                                    )}{" "}
                                                    {
                                                        investigation.case_id
                                                    }
                                                </p>
                                            </div>

                                            <time
                                                dateTime={
                                                    investigation.timestamp
                                                }
                                                title={formatExactDate(
                                                    investigation.timestamp,
                                                )}
                                                className="shrink-0 text-sm text-slate-400"
                                            >
                                                {formatRelativeDate(
                                                    investigation.timestamp,
                                                )}
                                            </time>
                                        </div>
                                    </button>
                                ),
                            )}
                        </div>
                    </Card>
                )}
        </section>
    );
}


export default RecentInvestigations;