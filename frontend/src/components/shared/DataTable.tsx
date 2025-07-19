import {
    type ColumnDef,
    type ColumnFiltersState,
    flexRender,
    getCoreRowModel,
    getFilteredRowModel,
    useReactTable,
} from "@tanstack/react-table";
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow,} from "@/components/ui/table.tsx";
import {useState} from "react";
import {Input} from "@/components/ui/input.tsx";
import {LucideSearch} from "lucide-react";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select.tsx";

type DataTableProps<TData, TValue> = {
    columns: ColumnDef<TData, TValue>[];
    data: TData[];
    className?: string;
};

export function DataTable<TData, TValue>({
                                             columns,
                                             data,
                                             className,
                                         }: DataTableProps<TData, TValue>) {

    const [filters, setFilters] = useState<ColumnFiltersState>([]);


    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
        onColumnFiltersChange: setFilters,
        getFilteredRowModel: getFilteredRowModel(),
        state: {
            columnFilters: filters,
        }
    });

    console.log("Filtered rows:", table.getFilteredRowModel().rows);

    return (
        <>
            <div className="flex justify-between gap-4">

                <div className="relative w-full">
                    <Input
                        className="pl-8"
                        placeholder="Search workflows..."
                        value={(table.getColumn("name")?.getFilterValue() as string) ?? ""}
                        onChange={(event) =>
                            table.getColumn("name")?.setFilterValue(event.target.value)
                        }
                    />
                    <LucideSearch className="absolute top-1/2 left-2 size-4 -translate-y-1/2 opacity-50 select-none"/>
                </div>

                <Select defaultValue="all">
                    <SelectTrigger className="w-[180px]">
                        <SelectValue/>
                    </SelectTrigger>
                    <SelectContent>
                        <SelectGroup>
                            <SelectLabel>Filter</SelectLabel>
                            <SelectItem value="all">All Workflows</SelectItem>
                            <SelectItem value="active">Active Workflows</SelectItem>
                            <SelectItem value="inactive">Inactive Workflows</SelectItem>
                        </SelectGroup>
                    </SelectContent>
                </Select>

            </div>
            <div className={`rounded-md border bg-sidebar ${className}`}>
                <Table>
                    <TableHeader className="bg-sidebar-accent">
                        {table.getHeaderGroups().map((headerGroup) => (
                            <TableRow key={headerGroup.id}>
                                {headerGroup.headers.map((header) => (
                                    <TableHead key={header.id}>
                                        {header.isPlaceholder
                                            ? null
                                            : flexRender(
                                                header.column.columnDef.header,
                                                header.getContext()
                                            )}
                                    </TableHead>
                                ))}
                            </TableRow>
                        ))}
                    </TableHeader>
                    <TableBody>
                        {table.getRowModel().rows.map((row) => (
                            <TableRow key={row.id}>
                                {row.getVisibleCells().map((cell) => (
                                    <TableCell key={cell.id} className="p-4">
                                        {flexRender(
                                            cell.column.columnDef.cell,
                                            cell.getContext()
                                        )}
                                    </TableCell>
                                ))}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        </>
    );
}

