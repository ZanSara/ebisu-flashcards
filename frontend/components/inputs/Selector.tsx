import { useState } from "react";

export interface SelectorOption {
  name: string;
  color: string;
}

interface SelectorProps {
  className?: string;
  options: SelectorOption[];
  onChange(selection: any): any;
}

/**
 * Depending on the selection state, generates different styles for the buttons
 * @param selected if the button is selected or not
 * @param color the name of the color (e.g. red, blue)
 */
function getConditionalButtonStyle(selected: boolean, color: string): string {
  if (selected) {
    return `bg-${color}-500 text-white font-bold`;
  } else {
    return `bg-${color}-200 hover:bg-${color}-300`;
  }
}

const Selector = (props: SelectorProps) => {
  const [selectedOption, setSelectedOption] = useState<SelectorOption>();

  return (
    <div className={`flex gap-2 rounded-xl overflow-hidden ${props.className}`}>
      {props.options.map((opt) => {
        const selected = opt.name === selectedOption?.name;
        const extraStyle = getConditionalButtonStyle(selected, opt?.color);

        return (
          <button
            key={opt.name}
            className={`flex-grow text-center py-2 transition-colors ${extraStyle}`}
            onClick={(e) => {
              e.preventDefault(); // Prevent the default event happening (i.e. posting the form)
              setSelectedOption(opt); // Set the option as selected
              props.onChange(opt); // Notify the parent element of the change
            }}
          >
            {opt.name}
          </button>
        );
      })}
    </div>
  );
};

export default Selector;
