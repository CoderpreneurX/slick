import * as React from "react";
import { cn } from "@/lib/utils";

interface InputProps extends React.ComponentProps<"input"> {
  icon?: React.ReactNode;
}

function Input({ className, type, icon, ...props }: InputProps) {
  const [isFocused, setIsFocused] = React.useState(false);
  const hasIcon = !!icon;

  return (
    <div className="relative">
      {hasIcon && (
        <div
          className={cn(
            "absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none transition-colors",
            isFocused ? "text-primary" : "text-muted-foreground"
          )}
        >
          {icon}
        </div>
      )}

      <input
        type={type}
        data-slot="input"
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        className={cn(
          "file:text-foreground placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground dark:bg-input/30 flex border border-secondary focus:border-primary focus-visible:border-primary focus-within:border-primary h-9 w-full min-w-0 bg-transparent py-1 text-base shadow-xs transition-[color,box-shadow] outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
          hasIcon ? "pl-10" : "px-3",
          className
        )}
        {...props}
      />
    </div>
  );
}

export { Input };
