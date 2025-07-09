import {cn} from "@/lib/utils"
import {Button} from "@/components/ui/button"
import {
    Card,
    CardContent,
} from "@/components/ui/card"
import {Input} from "@/components/ui/input"
import {Label} from "@/components/ui/label"
import * as React from "react";
import {Separator} from "@/components/ui/separator.tsx";

export function LoginForm({
                              className,
                              ...props
                          }: React.ComponentProps<"div">) {
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
                                <a
                                    href="#"
                                    className="ml-auto inline-block text-sm underline-offset-4 hover:underline text-primary"
                                >
                                    Forgot your password?
                                </a>
                            </div>

                            <Button type="submit" className="w-full">
                                Login
                            </Button>
                        </div>
                        <div className="mt-6 flex items-center gap-2">
                            <Separator className="flex-1"/>
                            <span className="text-muted-foreground text-sm">New to Hookline?</span>
                            <Separator className="flex-1"/>
                        </div>
                        <Button variant="outline" className="w-full mt-6">
                            Create a new account
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}
