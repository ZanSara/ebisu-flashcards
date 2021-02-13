import { FunctionComponent } from "react";

export interface LinkButtonProps {
  color: string;
  title: string;
  href: string;
}

const LinkButton: FunctionComponent<LinkButtonProps> = (props) => {
  const colorStyle = `bg-${props.color}-200 hover:bg-${props.color}-400`;

  return (
    <a href={props.href} className={`${colorStyle} py-1.5 px-4 rounded-xl font-medium transition-colors shadow-sm`}>
      {props.title}
    </a>
  );
};

export default LinkButton;
