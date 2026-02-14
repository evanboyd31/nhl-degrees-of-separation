export interface Player {
  id: number;
  full_name: string;
  headshot_url: string;
}

export interface TeamPeriod {
  tricode: string;
  startYear: number;
  endYear: number;
  primaryColor: string;
  secondaryColor: string;
}
