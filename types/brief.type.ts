interface IProject {
  ID: string;
  title: string;
  authors: string;
  'authors-array': string[];
  'final-proposition': string;
  insights: string;
  videoURL: string;
  thumbURL: string;
}

interface IBrief {
  briefNumber: string;
  title: string;
  items: IProject[];
}

export type { IProject, IBrief };
