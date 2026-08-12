"""
Command-Line Interface (CLI) for Lead Intelligence Platform.
"""

import sys
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.config.settings import settings
from src.database.repository import SQLiteCompanyRepository
from src.discovery.ingestion import IngestionService
from src.logging.logger import logger
from src.utils.exceptions import LeadIntelException

console = Console()
VERSION = "0.1.0"


def print_banner():
    """Prints styled CLI application banner."""
    console.print(
        Panel.fit(
            f"[bold cyan]Lead Intelligence Platform[/bold cyan] [yellow]v{VERSION}[/yellow]\n"
            "[dim]B2B Business Lead Discovery & Digital Posture Audit Engine[/dim]",
            border_style="cyan"
        )
    )


def cmd_version():
    """Output version and environment info."""
    print_banner()
    console.print(f"[bold green]Version:[/bold green] {VERSION}")
    console.print(f"[bold green]Environment:[/bold green] {settings.environment}")
    console.print(f"[bold green]Target Market:[/bold green] {settings.discovery.default_country} ({', '.join(settings.discovery.default_industries)})")


def cmd_config():
    """Output current application settings table."""
    print_banner()
    table = Table(title="Application Configuration", show_header=True, header_style="bold magenta")
    table.add_column("Setting Parameter", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("App Name", settings.app_name)
    table.add_row("Environment", settings.environment)
    table.add_row("Debug Mode", str(settings.debug))
    table.add_row("SQLite DB Path", str(settings.database.sqlite_db_path))
    table.add_row("Default Country", settings.discovery.default_country)
    table.add_row("Default Industries", ", ".join(settings.discovery.default_industries))
    table.add_row("Confidence Threshold", str(settings.discovery.confidence_threshold))

    console.print(table)


def cmd_ingest_domain(domain: str, name: str | None, industry: str, country: str):
    """Ingest a single target company domain."""
    print_banner()
    repo = SQLiteCompanyRepository()
    service = IngestionService(repo)

    try:
        company = service.ingest_single_domain(
            domain=domain,
            name=name,
            industry=industry,
            country=country
        )
        console.print(f"\n[bold green][OK] Company Target Registered Successfully![/bold green]")
        console.print(f"[cyan]ID:[/cyan] {company.id}")
        console.print(f"[cyan]Domain:[/cyan] {company.domain}")
        console.print(f"[cyan]Name:[/cyan] {company.name.value} (Confidence: {company.name.confidence})")
        console.print(f"[cyan]Industry:[/cyan] {company.industry.value}")
        console.print(f"[cyan]Country:[/cyan] {company.country.value}")
    except LeadIntelException as err:
        console.print(f"\n[bold red][ERROR] Ingestion Failed:[/bold red] {err}")
        sys.exit(1)


def cmd_ingest_file(file_path: str):
    """Ingest bulk targets from file."""
    print_banner()
    repo = SQLiteCompanyRepository()
    service = IngestionService(repo)

    try:
        summary = service.ingest_file(file_path)
        console.print(f"\n[bold green][OK] Bulk Ingestion Summary:[/bold green]")
        console.print(f"[cyan]Total Processed:[/cyan] {summary.total_processed}")
        console.print(f"[cyan]Successfully Added:[/cyan] {summary.added_count}")
        console.print(f"[yellow]Skipped Duplicates:[/yellow] {summary.duplicate_count}")
        console.print(f"[red]Errors Encountered:[/red] {summary.error_count}")
    except LeadIntelException as err:
        console.print(f"\n[bold red][ERROR] File Ingestion Failed:[/bold red] {err}")
        sys.exit(1)


def cmd_list_targets():
    """List all registered target companies in repository."""
    print_banner()
    repo = SQLiteCompanyRepository()
    companies = repo.list_all()

    if not companies:
        console.print("[dim]No target companies registered yet in storage.[/dim]")
        return

    table = Table(title=f"Registered Targets ({len(companies)} Total)", show_header=True, header_style="bold cyan")
    table.add_column("Domain", style="yellow")
    table.add_column("Business Name", style="bold green")
    table.add_column("Industry", style="blue")
    table.add_column("Country", style="magenta")
    table.add_column("Status", style="cyan")

    for c in companies:
        table.add_row(
            c.domain,
            c.name.value or "N/A",
            c.industry.value or "N/A",
            c.country.value or "N/A",
            c.status.value
        )

    console.print(table)


def cmd_enrich_domain(domain: str, verbose: bool = False):
    """Enrich a target company domain with website intelligence."""
    import asyncio
    from src.enrichment.enrichment_pipeline import EnrichmentPipeline

    print_banner()
    repo = SQLiteCompanyRepository()
    pipeline = EnrichmentPipeline(repository=repo)

    company = repo.get_by_domain(domain)
    if not company:
        console.print(f"[yellow]Target domain '{domain}' not found in storage. Registering new target...[/yellow]")
        from src.discovery.ingestion import IngestionService
        service = IngestionService(repo)
        company = service.ingest_single_domain(domain=domain)

    console.print(f"[bold cyan]Running Website Intelligence Enrichment for '{company.domain}'...[/bold cyan]")
    report = asyncio.run(pipeline.enrich_company(company))

    console.print(f"\n[bold green][OK] Website & Technical Enrichment Completed in {report.execution_time_seconds}s[/bold green]")
    console.print(f"[cyan]Title:[/cyan] {report.metadata.title or 'N/A'}")
    console.print(f"[cyan]CMS Detected:[/cyan] {report.cms.cms_name.value} (Confidence: {report.cms.confidence})")
    console.print(f"[cyan]Emails Discovered:[/cyan] {', '.join(report.contacts.emails) or 'None'}")
    console.print(f"[cyan]Phones Discovered:[/cyan] {', '.join(report.contacts.phone_numbers) or 'None'}")
    console.print(f"[cyan]Social Links:[/cyan] Facebook={report.socials.facebook or 'N/A'}, LinkedIn={report.socials.linkedin or 'N/A'}")
    console.print(f"[cyan]Robots.txt:[/cyan] {'Found' if report.robots.is_found else 'Not Found'}, Sitemap URLs={len(report.sitemap.sitemap_urls)}")

    if report.seo:
        console.print(f"[cyan]SEO Posture:[/cyan] H1 Tags={report.seo.data.h1_count}, Indexable={report.seo.data.is_indexable}, ALT Coverage={report.seo.data.image_alt_coverage_ratio * 100}%")
    if report.tech_stack:
        tech_names = [t.name for cat in (report.tech_stack.data.analytics, report.tech_stack.data.advertising, report.tech_stack.data.js_frameworks, report.tech_stack.data.infrastructure) for t in cat]
        console.print(f"[cyan]Tech Stack:[/cyan] {', '.join(tech_names) or 'Standard Web Server'}")
    if report.performance:
        console.print(f"[cyan]Performance:[/cyan] Response Latency={report.performance.data.response_time_ms}ms, Page Weight={round(report.performance.data.page_size_bytes / 1024, 1)}KB")
    if report.accessibility:
        console.print(f"[cyan]Accessibility Score:[/cyan] {report.accessibility.data.accessibility_score}/100")
    if report.security:
        console.print(f"[cyan]Security Header Score:[/cyan] {report.security.data.security_score}/100 (HSTS={'Yes' if report.security.data.has_strict_transport_security else 'No'}, CSP={'Yes' if report.security.data.has_content_security_policy else 'No'})")
    if hasattr(report, "contact_discovery") and report.contact_discovery:
        cd = report.contact_discovery
        email_str = ", ".join([f"{e.address} ({e.category.value})" for e in cd.emails]) or "None"
        phone_str = ", ".join([f"{p.formatted_number} ({p.category.value})" for p in cd.phones]) or "None"
        console.print(f"[bold yellow]Contact Discovery:[/bold yellow] Emails={email_str}")
        console.print(f"[bold yellow]Phones (E.164):[/bold yellow] {phone_str}")
        if cd.addresses:
            console.print(f"[bold yellow]Physical Address:[/bold yellow] {cd.addresses[0].raw_address}")
    if hasattr(report, "decision_maker_discovery") and report.decision_maker_discovery:
        dm_rep = report.decision_maker_discovery
        console.print(f"\n[bold green]Decision Maker Discovery (Phase 04):[/bold green]")
        console.print(f"  [cyan]Leadership Pages Discovered:[/cyan] {len(dm_rep.leadership_pages)}")
        for page in dm_rep.leadership_pages[:3]:
            console.print(f"    • [dim]{page.url} (Source: {page.source}, Confidence: {page.confidence * 100:.0f}%)[/dim]")
        
        console.print(f"  [cyan]Decision Makers Identified:[/cyan] {dm_rep.total_people_found}")
        if dm_rep.decision_makers:
            for dm in dm_rep.decision_makers:
                console.print(
                    f"    • [bold white]{dm.full_name}[/bold white] - [cyan]{dm.normalized_title}[/cyan] "
                    f"([magenta]{dm.department.value}[/magenta] | Seniority: {dm.seniority.value}) "
                    f"[yellow]Priority: {dm.priority}[/yellow] | [green]Confidence: {dm.confidence * 100:.0f}%[/green]"
                )
                contact_bits = []
                if dm.email:
                    contact_bits.append(f"Email: {dm.email}")
                if dm.phone:
                    contact_bits.append(f"Phone: {dm.phone}")
                if dm.linkedin_url:
                    contact_bits.append(f"LinkedIn: {dm.linkedin_url}")
                if contact_bits:
                    console.print(f"      [dim]{' | '.join(contact_bits)}[/dim]")
        else:
            console.print("    [dim]• No verified decision makers found on public leadership pages.[/dim]")

    if hasattr(report, "business_intelligence") and report.business_intelligence:
        bi = report.business_intelligence
        console.print(f"\n[bold green]Business Intelligence (Phase 05):[/bold green]")
        console.print(f"  • [cyan]Industry:[/cyan] [bold white]{bi.industry.value}[/bold white] (Confidence: {bi.industry_confidence * 100:.0f}%) | [cyan]Business Model:[/cyan] {bi.business_model.value}")
        console.print(f"  • [cyan]Company Size:[/cyan] {bi.company_size_tier.value} | Est. Employees: [bold white]{bi.estimated_employee_range}[/bold white] (Confidence: {bi.company_size_confidence * 100:.0f}%)")
        if bi.years_in_business:
            console.print(f"  • [cyan]Years in Business:[/cyan] [bold white]{bi.years_in_business} years[/bold white] (Founded: {bi.founded_year})")
        if bi.primary_services:
            console.print(f"  • [cyan]Primary Services:[/cyan] {', '.join(bi.primary_services)}")
        if bi.secondary_services:
            console.print(f"  • [cyan]Secondary Services:[/cyan] {', '.join(bi.secondary_services)}")
        if bi.geography and (bi.geography.primary_headquarters or bi.geography.service_areas):
            hq = bi.geography.primary_headquarters or 'N/A'
            areas = ', '.join(bi.geography.service_areas[:4]) or 'Local'
            console.print(f"  • [cyan]Headquarters:[/cyan] {hq} | [cyan]Service Areas:[/cyan] {areas} (Offices: {bi.geography.office_locations_count})")
        if bi.trust_signals:
            ts = bi.trust_signals
            trust_bits = []
            if ts.has_testimonials: trust_bits.append("Testimonials")
            if ts.has_case_studies: trust_bits.append("Case Studies")
            if ts.has_portfolio: trust_bits.append("Portfolio")
            if ts.has_financing: trust_bits.append("Financing Options")
            if ts.has_warranty: trust_bits.append("Warranty Guarantees")
            if ts.certifications: trust_bits.append(f"Certs: {', '.join(ts.certifications)}")
            if ts.awards: trust_bits.append(f"Awards: {', '.join(ts.awards)}")
            if trust_bits:
                console.print(f"  • [cyan]Trust Signals:[/cyan] {', '.join(trust_bits)}")
        if bi.hiring:
            hiring_status = "Currently Hiring" if bi.hiring.currently_hiring else "No Active Hiring Signals"
            careers_str = f" (Careers: {bi.hiring.careers_page_url})" if bi.hiring.careers_page_url else ""
            console.print(f"  • [cyan]Hiring Status:[/cyan] {hiring_status}{careers_str}")

    if verbose:
        console.print("\n[bold magenta]--- Detailed Analyzer Findings & Warnings ---[/bold magenta]")
        for analyzer_obj in (report.seo, report.structured_data, report.tech_stack, report.performance, report.accessibility, report.links, report.security):
            if analyzer_obj:
                console.print(f"\n[bold underline]{analyzer_obj.analyzer_name}[/bold underline]")
                for f in analyzer_obj.findings:
                    console.print(f"  [green][OK] {f}[/green]")
                for w in analyzer_obj.warnings:
                    console.print(f"  [yellow][WARN] {w}[/yellow]")


def main():
    """Main CLI Entrypoint."""
    parser = argparse.ArgumentParser(description="Lead Intelligence Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # discover subcommand group
    discover_parser = subparsers.add_parser("discover", help="Target company discovery operations")
    discover_subparsers = discover_parser.add_subparsers(dest="discover_command")

    # discover ingest
    ingest_parser = discover_subparsers.add_parser("ingest", help="Ingest a single domain target")
    ingest_parser.add_argument("-d", "--domain", required=True, help="Target business domain (e.g. roofingpro.com.au)")
    ingest_parser.add_argument("-n", "--name", help="Business name")
    ingest_parser.add_argument("-i", "--industry", default="Roofing", help="Industry sector")
    ingest_parser.add_argument("-c", "--country", default="Australia", help="Country location")

    # discover load
    load_parser = discover_subparsers.add_parser("load", help="Ingest bulk targets from file (CSV/JSON/TXT)")
    load_parser.add_argument("-f", "--file", required=True, help="Path to seed file")

    # discover list
    discover_subparsers.add_parser("list", help="List registered company targets")

    # enrich subcommand
    enrich_parser = subparsers.add_parser("enrich", help="Run website intelligence enrichment on a target domain")
    enrich_parser.add_argument("-d", "--domain", required=True, help="Target business domain to enrich")
    enrich_parser.add_argument("-v", "--verbose", action="store_true", help="Display detailed analyzer findings and warnings")

    # config & version
    subparsers.add_parser("config", help="Display application configuration")
    subparsers.add_parser("version", help="Display platform version")

    args = parser.parse_args()

    if args.command == "version":
        cmd_version()
    elif args.command == "config":
        cmd_config()
    elif args.command == "enrich":
        cmd_enrich_domain(args.domain, verbose=args.verbose)
    elif args.command == "discover":
        if args.discover_command == "ingest":
            cmd_ingest_domain(args.domain, args.name, args.industry, args.country)
        elif args.discover_command == "load":
            cmd_ingest_file(args.file)
        elif args.discover_command == "list":
            cmd_list_targets()
        else:
            discover_parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
