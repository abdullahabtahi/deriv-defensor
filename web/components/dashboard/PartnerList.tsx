"use client"

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ChevronRight, ArrowDownRight } from "lucide-react"
import Link from "next/link"


interface PartnerListProps {
    partners: any[]
}


export function PartnerList({ partners }: PartnerListProps) {


    return (
        <div className="rounded-md border">
            <Table>
                <TableHeader>
                    <TableRow className="bg-gray-50/50">
                        <TableHead className="w-[100px]">Partner ID</TableHead>
                        <TableHead>Region</TableHead>
                        <TableHead>Tier</TableHead>
                        <TableHead className="text-right">Churn Prob</TableHead>
                        <TableHead className="text-right">Action</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {partners.map((partner) => (
                        <TableRow key={partner.partner_id}>
                            <TableCell className="font-medium text-deriv-blue">{partner.partner_id}</TableCell>
                            <TableCell>{partner.region}</TableCell>
                            <TableCell>
                                <Badge variant="outline" className="border-gray-300 text-gray-600 font-medium">
                                    {partner.tier}
                                </Badge>
                            </TableCell>
                            <TableCell className="text-right">
                                <div className="flex flex-col items-end">
                                    <span className="text-deriv-red font-bold">{(partner.churn_prob * 100).toFixed(0)}%</span>
                                    <span className="text-xs text-gray-400 flex items-center">
                                        <ArrowDownRight size={12} className="text-deriv-red mr-1" />
                                        trending
                                    </span>
                                </div>
                            </TableCell>
                            <TableCell className="text-right">
                                <Link href={`/partners/${partner.partner_id}`}>
                                    <Button size="sm" variant="ghost" className="h-8 w-8 p-0">
                                        <ChevronRight size={16} />
                                    </Button>
                                </Link>
                            </TableCell>

                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    )
}
