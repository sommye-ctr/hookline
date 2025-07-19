export interface WorkflowModel {
    id: number;
    name: string;
    description: string;
    isActive: boolean;
    actions: string[];
    executionCount: number;
    lastExecution: Date;
    triggers: string[];
}
