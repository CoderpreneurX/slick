import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "relative font-bold inline-flex items-center justify-center font-medium overflow-hidden group border transition-colors duration-300",
  {
    variants: {
      variant: {
        default:
          "border border-primary bg-primary text-background hover:text-primary",
        outline:
          "border border-secondary text-secondary bg-background hover:text-background",
        ghost:
          "bg-transparent text-foreground hover:bg-accent/10 hover:text-accent-foreground",
        destructive: "bg-destructive text-white hover:bg-destructive/80",
        alert:
          "border-accent text-accent hover:text-primary hover:border-primary",
      },
      size: {
        default: "h-9 px-6 py-3 has-[>svg]:px-3",
        sm: "h-8 gap-1.5 px-3 has-[>svg]:px-2.5",
        lg: "h-10 px-6 has-[>svg]:px-4",
        icon: "size-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

function Button({
  className,
  variant = "default",
  size,
  asChild = false,
  disabled,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean;
  }) {
  const Comp = asChild ? Slot : "button";

  return (
    <Comp
      data-slot="button"
      className={cn(
        "group relative overflow-hidden", // Ensure hover works
        buttonVariants({ variant, size }),
        className,
        disabled ? "cursor-not-allowed" : "cursor-pointer"
      )}
      disabled={disabled}
      {...props}
    >
      {/* Foreground content */}
      <span className="relative z-10 transition-colors duration-300">
        {props.children}
      </span>

      {/* Overlay background span */}
      <span
        className={cn(
          "absolute inset-0 transition-all duration-300 ease-out z-0",
          disabled ? "w-full opacity-75" : "w-0 group-hover:w-full",
          variant === "default" && "bg-background",
          variant === "outline" && "bg-secondary",
          variant === "alert" && "bg-accent"
        )}
      />
    </Comp>
  );
}

export { Button, buttonVariants };
