import { api } from "@/services/api"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Calendar, User, CheckCircle2, Clock } from "lucide-react"

export default async function InterventionsPage() {
    const interventions = await api.getInterventions()

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Intervention Log</h1>
                    <p className="text-gray-500 text-sm">Tracking all retention actions and their outcomes.</p>
                </div>
            </div>

            <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
                <Table>
                    <TableHeader>
                        <TableRow className="bg-gray-50">
                            <TableHead className="w-[180px]">Timestamp</TableHead>
                            <TableHead>Partner</TableHead>
                            <TableHead>Action Type</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Performed By</TableHead>
                            <TableHead className="text-right">Outcome</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {interventions.map((log: any) => (
                            <TableRow key={log.id}>
                                <TableCell className="text-sm text-gray-500 flex items-center gap-2">
                                    <Clock size={14} />
                                    {new Date(log.timestamp).toLocaleString()}
                                </TableCell>
                                <TableCell className="font-medium text-deriv-blue">{log.partner_id}</TableCell>
                                <TableCell>
                                    <span className="text-sm font-medium">{log.action_type}</span>
                                </TableCell>
                                <TableCell>
                                    <Badge
                                        variant="outline"
                                        className={
                                            log.status === 'Completed'
                                                ? 'bg-green-50 text-green-700 border-green-200'
                                                : log.status === 'Failed'
                                                    ? 'bg-red-50 text-red-700 border-red-200'
                                                    : 'bg-blue-50 text-blue-700 border-blue-200'
                                        }
                                    >
                                        {log.status}
                                    </Badge>
                                </TableCell>
                                <TableCell className="text-sm text-gray-600 flex items-center gap-2">
                                    <User size={14} />
                                    {log.performed_by}
                                </TableCell>
                                <TableCell className="text-right font-medium text-deriv-green">
                                    {log.outcome_label || "Pending"}
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        </div>
    )
}
