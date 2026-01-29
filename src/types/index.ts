export interface Worktree {
    name: string;
    path: string;
    branch: string;
}

export interface WorkflowRoles {
    planner: Worktree;
    implementer: Worktree;
    reviewer: Worktree;
}

export interface WorkflowConfig {
    feature: string;
    roles: WorkflowRoles;
}