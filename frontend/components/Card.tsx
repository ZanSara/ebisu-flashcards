import { FunctionComponent } from "react";

export interface CardProps {
  className: string;
}

const Card: FunctionComponent<CardProps> = (props) => {
  return <div className={`shadow-sm rounded-xl ${props.className}`}>{props.children}</div>;
};

export default Card;
