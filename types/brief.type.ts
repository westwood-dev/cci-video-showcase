interface IPosition {
  x: number;
  y: number;
  id: number;
}

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

interface IFocused {
  id: string;
  layerIndex: number;
  itemIndex: number;
  initialRect: DOMRect;
  animating: boolean;
  itemData: IProject;
}

export type { IPosition, IProject, IBrief, IFocused };
