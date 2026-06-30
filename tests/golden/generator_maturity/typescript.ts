/** Account response model. */
export interface Account {
  /** Stable account identifier. */
  id: string;
  /** Current subscription plan. */
  plan: Plan;
  /** Operational account status. */
  status: "active" | "suspended";
  /** Searchable account labels. */
  tags?: string[];
  /** Public profile details. */
  profile?: { displayName: string; age?: number };
  /** Account contact methods. */
  contacts?: { email: string; primary?: boolean }[];
  /** Optional display nickname. */
  nickname?: string | null;
}

/** Subscription plan summary. */
export interface Plan {
  /** Commercial plan tier. */
  tier: "free" | "pro";
}
