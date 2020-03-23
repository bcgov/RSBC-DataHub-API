--=-=-=-=-=-=-=-=-=-=  CREATE  ETK TABLES  =-=-=-=-=-=-=-=-=-=--
USE [rsbcodw]
GO

/****** Object:  Table [etk].[events] ******/
DROP TABLE IF EXISTS [etk].[events]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [etk].[events](
	[id] [bigint] NOT NULL,
	[date_time] [date] NOT NULL,
	[type] [varchar](100) NOT NULL,
	[version] [varchar](10) NOT NULL
) ON [PRIMARY]
GO



/****** Object:  Table [etk].[violations] ******/
DROP TABLE IF EXISTS [etk].[violations]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [etk].[violations](
	[count_number] [tinyint] NOT NULL,
	[ticket_number] [varchar](100) NOT NULL,
	[act_code] [varchar](400) NOT NULL,
	[section_text] [varchar](400) NOT NULL,
	[section_desc] [varchar](400) NOT NULL,
	[fine_amount] [varchar](400) NOT NULL,
 CONSTRAINT [pk_violations] PRIMARY KEY CLUSTERED 
(
	[count_number] ASC,
	[ticket_number] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


/****** Object:  Table [etk].[issuance] ******/
DROP TABLE IF EXISTS [etk].[issuances]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [etk].[issuances](
	[event_id] [bigint] NOT NULL,
    [submit_date] [date] NOT NULL,
    [sent_time] [varchar](400) NOT NULL,
    [ticket_number] [varchar](400) NOT NULL,
    [drivers_licence_province_code] [varchar](400) NULL,
    [person_gender_code] [varchar](400) NULL,
    [person_residence_city_name] [varchar](400) NULL,
    [person_residence_province_code] [varchar](400) NULL,
    [young_person_yn] [varchar](400) NULL,
    [offender_type_code] [varchar](400) NULL,
    [violation_date] [date] NOT NULL,
    [violation_time] [varchar](400) NOT NULL,
    [violation_highway_desc] [varchar](400) NULL,
    [violation_city_code] [varchar](400) NULL,
    [violation_city_name] [varchar](400) NULL,
    [vehicle_province_code] [varchar](400) NULL,
    [vehicle_nsj_puj_cd] [varchar](400) NULL,
    [vehicle_make_code] [varchar](400) NULL,
    [vehicle_type_code] [varchar](400) NULL,
    [vehicle_year] [varchar](400) NULL,
    [accident_yn] [varchar](400) NULL,
    [dispute_address_text] [varchar](400) NULL,
    [court_location_code] [varchar](400) NULL,
    [mre_agency_text] [varchar](400) NULL,
    [enforcement_jurisdiction_code] [varchar](400) NOT NULL,
    [certificate_of_service_date] [date] NOT NULL,
    [certificate_of_service_number] [varchar](400) NOT NULL,
    [e_violation_form_number] [varchar](400) NOT NULL,
    [enforcement_jurisdiction_name] [varchar](400) NULL,
    [mre_minor_version_text] [varchar](400) NULL,
    [count_quantity] [tinyint] NULL,
    [enforcement_officer_number] [varchar](400) NULL,
    [enforcement_officer_name] [varchar](400) NULL,
    [ent_date] [date] NULL,
 CONSTRAINT [pk_issuance] PRIMARY KEY CLUSTERED 
(
	[event_id] ASC,
	[ticket_number] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


/****** Object:  Table [etk].[payments] ******/
DROP TABLE IF EXISTS [etk].[payments]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [etk].[payments](
	[event_id] [bigint] NOT NULL,
	[count_number] [tinyint] NOT NULL,
	[ticket_number] [varchar](100) NOT NULL,
	[payment_card_type] [varchar](400) NOT NULL,
	[payment_ticket_type_code] [varchar](400) NOT NULL,
	[payment_amount] [int] NOT NULL,
 CONSTRAINT [pk_payments] PRIMARY KEY CLUSTERED 
(
	[event_id] ASC,
	[count_number] ASC,
	[ticket_number] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


/****** Object:  Table [etk].[query] ******/
DROP TABLE IF EXISTS [etk].[queries]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [etk].[queries](
	[event_id] [bigint] NOT NULL,
	[ticket_number] [varchar](100) NOT NULL,
 CONSTRAINT [pk_query] PRIMARY KEY CLUSTERED 
(
	[event_id] ASC,
	[ticket_number] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


/****** Object:  Table [etk].[dispute] ******/
DROP TABLE IF EXISTS [etk].[disputes]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [etk].[disputes](
	[event_id] [bigint] NOT NULL,
	[count_number] [tinyint] NOT NULL,
	[ticket_number] [varchar](100) NOT NULL,
	[dispute_action_date] [varchar](400) NOT NULL,
	[dispute_type_code] [varchar](400) NOT NULL,
	[count_act_regulation] [varchar](400) NOT NULL,
	[compressed_section] [varchar](400) NOT NULL,
 CONSTRAINT [pk_dispute] PRIMARY KEY CLUSTERED 
(
	[event_id] ASC,
	[count_number] ASC,
	[ticket_number] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO



/****** Object:  Table [etk].[dispute_status_update] ******/
DROP TABLE IF EXISTS [etk].[dispute_status_updates]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [etk].[dispute_status_updates](
	[event_id] [bigint] NOT NULL,
	[count_number] [tinyint] NOT NULL,
	[ticket_number] [varchar](100) NOT NULL,
	[dispute_action_date] [varchar](400) NOT NULL,
	[dispute_action_code] [varchar](400) NOT NULL,
 CONSTRAINT [pk_dispute_status_update] PRIMARY KEY CLUSTERED 
(
	[event_id] ASC,
	[count_number] ASC,
	[ticket_number] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


/****** Object:  Table [etk].[dispute_finding] ******/
DROP TABLE IF EXISTS [etk].[dispute_findings]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [etk].[dispute_findings](
	[event_id] [bigint] NOT NULL,
	[count_number] [tinyint] NOT NULL,
	[ticket_number] [varchar](100) NOT NULL,
	[finding_date] [varchar](400) NOT NULL,
	[finding_code] [varchar](400) NOT NULL,
	[finding_description] [varchar](400) NOT NULL,
 CONSTRAINT [pk_dispute_finding] PRIMARY KEY CLUSTERED 
(
	[event_id] ASC,
	[count_number] ASC,
	[ticket_number] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
