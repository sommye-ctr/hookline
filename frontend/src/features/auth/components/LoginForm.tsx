import {cn} from "@/lib/utils.ts"
import {Button} from "@/components/ui/button.tsx"
import {
    Card,
    CardContent,
} from "@/components/ui/card.tsx"
import {Input} from "@/components/ui/input.tsx"
import {Label} from "@/components/ui/label.tsx"
import * as React from "react";
import {Separator} from "@/components/ui/separator.tsx";

interface LoginFormProps extends React.ComponentProps<"div"> {
    login: boolean,
    onSecondaryActionClicked?: () => void,
}

export function LoginForm({
                              className,
                              login,
                              onSecondaryActionClicked,
                              ...props
                          }: LoginFormProps) {
    return (
        <div className={cn("flex flex-col gap-6", className)} {...props}>
            <Card className="shadow-md">
                <CardContent>
                    <form>
                        <div className="flex flex-col gap-6">
                            <div className="grid gap-3">
                                <Label htmlFor="email">Email</Label>
                                <Input
                                    id="email"
                                    type="email"
                                    placeholder="m@example.com"
                                    required
                                />
                            </div>
                            <div className="flex flex-col gap-2">
                                <div className="grid gap-3">
                                    <Label htmlFor="password">Password</Label>
                                    <Input id="password" type="password" placeholder="••••••••••••" required/>
                                </div>
                                {login
                                    &&
                                    <a href="#"
                                       className="ml-auto inline-block text-sm underline-offset-4 hover:underline text-primary">
                                        Forgot your password?
                                    </a>
                                }

                            </div>

                            <Button type="submit" className="w-full">
                                {login ? "Login" : "Sign Up"}
                            </Button>
                        </div>
                        <div className="mt-6 flex items-center gap-2">
                            <Separator className="flex-1"/>
                            <span className="text-muted-foreground text-sm">
                                {login ? "New to Hookline?" : "Already have an account?"}
                            </span>
                            <Separator className="flex-1"/>
                        </div>
                        <Button variant="outline" className="w-full mt-6" onClick={onSecondaryActionClicked}>
                            {login ? "Create a new account" : "Sign into existing account"}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}
