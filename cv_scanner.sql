-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Aug 19, 2019 at 03:37 PM
-- Server version: 10.1.10-MariaDB
-- PHP Version: 5.6.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cv_scanner`
--

-- --------------------------------------------------------

--
-- Table structure for table `applied_jobs`
--

CREATE TABLE `applied_jobs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL,
  `rank` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `applied_jobs`
--

INSERT INTO `applied_jobs` (`id`, `user_id`, `job_id`, `rank`, `date`) VALUES
(137, 61, 19, 75, '2019-08-19 08:27:06'),
(138, 62, 19, 55, '2019-08-19 08:29:31'),
(140, 63, 19, 80, '2019-08-19 08:37:00');

-- --------------------------------------------------------

--
-- Table structure for table `education`
--

CREATE TABLE `education` (
  `edu_id` int(50) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `School_` varchar(50) NOT NULL,
  `Degree_` varchar(50) NOT NULL,
  `FOS_` varchar(50) NOT NULL,
  `Grade_` varchar(50) NOT NULL,
  `Act_sociies` varchar(50) NOT NULL,
  `from_` varchar(50) NOT NULL,
  `to_` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `education`
--

INSERT INTO `education` (`edu_id`, `user_id`, `School_`, `Degree_`, `FOS_`, `Grade_`, `Act_sociies`, `from_`, `to_`) VALUES
(1, '1', 'Stanford university', 'MSCS', '', '', '', '', ''),
(2, '2', 'PAF-KIET', 'BSCS', '', '', '', '', ''),
(3, '3', 'Harvard university', 'BSCS', '', '', '', '', ''),
(4, '4', 'IBA', 'MBA', '', '', '', '', ''),
(5, '5', 'Karachi University', 'BCOM', '', '', '', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `edu_data`
--

CREATE TABLE `edu_data` (
  `id` int(11) NOT NULL,
  `label` varchar(100) NOT NULL,
  `data` longtext NOT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `edu_data`
--

INSERT INTO `edu_data` (`id`, `label`, `data`, `score`) VALUES
(1, 'MSCS', 'MSCS,MS.CS,MS CS,MS-CS,MS - CS,MS in Computer Science, MS of Computer Science, MS Computer Science', 30),
(2, 'BSCS', 'BSCS,BS.CS,BS CS,BS-CS,BS - CS,BS in Computer Science,BS of Computer Science,BS Computer Science', 20),
(3, 'ICMAP', 'ICMAP,I.C.M.A.P,I-C-M-A-P ', 20),
(4, 'BE', 'BE,B.E,B-E,BE Electrical,BE in Electrical,B.E in Electronics,BE Electronics,Bachelors in Electronics', 20),
(5, 'LLB', 'LLB,L.L.B,L-L-B,Bachelors of Laws', 20),
(6, 'LLM', 'LLM,L.L.M,L-L-M,Master of Laws', 30),
(7, 'MSC', 'MSC,M.S.C,M-S-C,MSc,Masters of Science,M.Sc', 30),
(8, 'BS.c', 'BSC,B.S.C,B-S-C,BSc,Bachelors of Science,B.Sc', 20),
(9, 'MA', 'MA.M.A,M-A,Masters of Arts', 30),
(10, 'MBA', 'MBA,M.B.A,M-B-A,M B A,Master of Business Administration,Master of business administration,M.BA', 30),
(11, 'M.com', 'M.com,MCOM,Masters of Commerce,M-COM,M-com', 30),
(12, 'M.phill', 'M.phil,Masters of Philosophy,MPHIL,M-Phil,M-phil', 40),
(13, 'PHD', 'PHD,Ph.D,Doctor of Philosophy,P.H.D,P-H-D', 50),
(14, 'HSC', 'HSC,HSc,H.S.C,H-S-C,H S C,Inter,Intermediate', 10),
(15, 'BPA', 'BPA,Bachelors of Public Administration,B.P.A,B P A,B-P-A', 20),
(16, 'BBA', 'BBA,B.B.A,Bachelors of Business Administration,B B A,B-B-A', 20),
(17, 'DAE', 'DAE,Diploma of Associate Engineer,D.A.E,D A E,D-A-E', 10),
(18, 'CMA', 'CMA,Certified Management Accountant,C.M.A,C M A', 20),
(19, 'B.com', 'B.com,bcom,BCOM,Bcom,Bachelors of Commerce', 20),
(20, 'ACCA', 'ACCA,A.C.C.A,A C C A,Association of Chartered Certified Accountants', 20),
(21, 'CA', 'CA,Chartered accountant,C.A,C A,C-A', 30),
(22, 'ME', 'ME,M.E,M-E,ME Electrical,ME in Electrical,M.E in Electronics,ME Electronics,Masters in Electronics', 30),
(23, 'BA', 'BA.B.A,B-A,Bachelors of Arts', 20);

-- --------------------------------------------------------

--
-- Table structure for table `experience`
--

CREATE TABLE `experience` (
  `exp_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `company` varchar(50) NOT NULL,
  `location` varchar(50) NOT NULL,
  `duration` varchar(50) NOT NULL,
  `_desc` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `experience`
--

INSERT INTO `experience` (`exp_id`, `user_id`, `title`, `company`, `location`, `duration`, `_desc`) VALUES
(1, 1, 'Software Engineer', 'Google', '', '', ''),
(2, 2, 'Software Engineer', 'Avanza Solutions', '', '', ''),
(3, 3, 'Web Developer', 'Microsoft', '', '', ''),
(4, 4, 'Quality Control Supervisor', 'Huawei', '', '', ''),
(5, 5, 'Bank Manager', 'Meezan Bank', '', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `exp_data`
--

CREATE TABLE `exp_data` (
  `id` int(11) NOT NULL,
  `label` varchar(100) NOT NULL,
  `data` longtext NOT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `extract_cv`
--

CREATE TABLE `extract_cv` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `edu` varchar(255) NOT NULL,
  `exp` varchar(255) NOT NULL,
  `skill` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `job_posts`
--

CREATE TABLE `job_posts` (
  `id` int(50) NOT NULL,
  `company_name` varchar(50) NOT NULL,
  `company_loc` varchar(50) NOT NULL,
  `company_desc` longtext NOT NULL,
  `company_email` varchar(50) NOT NULL,
  `company_contact` varchar(50) NOT NULL,
  `job_title` varchar(50) NOT NULL,
  `job_loc` varchar(50) NOT NULL,
  `job_desc` longtext NOT NULL,
  `job_skill` varchar(500) NOT NULL,
  `job_qual` varchar(50) NOT NULL,
  `job_exp` varchar(100) NOT NULL,
  `salary` varchar(255) NOT NULL DEFAULT '10k-15k',
  `nature` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `job_posts`
--

INSERT INTO `job_posts` (`id`, `company_name`, `company_loc`, `company_desc`, `company_email`, `company_contact`, `job_title`, `job_loc`, `job_desc`, `job_skill`, `job_qual`, `job_exp`, `salary`, `nature`) VALUES
(19, 'PAF-KIET', 'Karachi', 'Private University', 'paf@pafkiet.edu.pk', '123456', 'Assistant Professor (Computer Science)', 'Karachi', 'Required an experienced Assistant Professor of Computer Science at PAF-KIET in Karachi. Interested candidate can apply.', 'C#,ASP.NET', 'MSCS', '5', '', ''),
(21, '10 Pearls', 'Lahore', 'a', 'tenpearls@gmail.com', '0', 'Senior Software Engineer', 'Lahore', 'Senior Software Engineer will develop information systems by studying operations; designing, developing and installing software solutions; support and develop software team. The Senior Software Engineer will lead a team of developers responsible for building new and support existing websites.', 'C#,ASP.NET,C++,Java', 'BSCS', '3', '', ''),
(22, 'Pakistan State Oil', 'a', 'a', 'pso@gov.com.pk', '1', 'Chartered Accountant', 'Karachi', 'As a chartered accountant you''ll give advice, audit accounts and provide trustworthy information about financial records. This might involve financial reporting, taxation, auditing, forensic accounting, corporate finance, business recovery and insolvency, or accounting systems and processes.', 'analytics,numeracy,accounting', 'CA', '8', '', ''),
(27, 'Folio3', 'Karachi', 'a', 'folio3@yahoo.com', '1', 'Android Developer', 'Islamabad', 'An Android developer is responsible for developing applications for devices powered by the Android operating system. Due to the fragmentation of this ecosystem, an Android developer must pay special attention to the application''s compatibility with multiple versions of Android and device types.', 'Android,XML,Java', 'BSCS', '2', '', ''),
(28, 'Siemens', 'a', 'a', 'Abc@gmail.com', '2', 'Electrical Engineer', 'Lahore', 'Electrical engineers design, develop, and test electrical devices and equipment, including communications systems, power generators, motors and navigation systems, and electrical systems for automobiles and aircraft. They also oversee the manufacture of these devices, systems, and equipment.', 'MATLAB,Micro Controller,Programming,C++', 'BE Electrical', '3', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `organization`
--

CREATE TABLE `organization` (
  `org_id` int(50) NOT NULL,
  `org_name` varchar(50) NOT NULL,
  `org_rank` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `organization`
--

INSERT INTO `organization` (`org_id`, `org_name`, `org_rank`) VALUES
(1, 'Google', 100),
(2, 'Samsung', 80),
(3, 'Citi Bank', 10),
(4, 'DHL', 50),
(5, 'IBM', 90);

-- --------------------------------------------------------

--
-- Table structure for table `personal_info`
--

CREATE TABLE `personal_info` (
  `Serial_No` int(11) NOT NULL,
  `_dob` varchar(50) NOT NULL,
  `_pno` varchar(50) NOT NULL,
  `_address` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `personal_info`
--

INSERT INTO `personal_info` (`Serial_No`, `_dob`, `_pno`, `_address`) VALUES
(1, 'sasasas', 'asass', 'ssss');

-- --------------------------------------------------------

--
-- Table structure for table `posted_jobs`
--

CREATE TABLE `posted_jobs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `posted_jobs`
--

INSERT INTO `posted_jobs` (`id`, `user_id`, `job_id`) VALUES
(421, 60, 19),
(422, 60, 21),
(423, 60, 22),
(428, 60, 27),
(429, 60, 28);

-- --------------------------------------------------------

--
-- Table structure for table `profile`
--

CREATE TABLE `profile` (
  `id` int(100) NOT NULL,
  `user_id` int(100) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(100) NOT NULL,
  `maritalstatus` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `cv` longtext NOT NULL,
  `qual` varchar(100) NOT NULL,
  `exp` varchar(100) NOT NULL,
  `skills` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `profile`
--

INSERT INTO `profile` (`id`, `user_id`, `dob`, `gender`, `maritalstatus`, `country`, `city`, `phone`, `cv`, `qual`, `exp`, `skills`) VALUES
(62, 60, '2019-08-19', 'Male', 'Unmarried', 'Pakistan', 'Karachi', '0322-1257134', 'Contact Information\n\n	A-472 Gulshan-e-Hadeed Phase 2 Karachi Bin Qasim-49\n\n	+92343-5628983\n\n	amirzada23@gmail.com\n\n\n\n	Job Sought\n\nSoftware Development\n\nWeb Development\n\nIT Admin Work\n\n\n\nAchievements\n\nWork on large E-commerce Websites \n\n\n\n\n\nSkills\n\nJava Programming\n\nC# Windows Forms\n\nASP.NET Web Forms\n\n\n\n\n\n  \n\n\n\n\n\n\n\n\n\n\n\nAMIR ZADA\n\n\n\nSummary\n\n\n\nTo work in a conductive learning environment where I can fully utilize my talent and applied knowledge to achieve efficiency and strive to promote the status of organization and to improve myself.\n\n\n\nWork Experience\n\n\n\nSenior Software Engineer                                                       2016 to date. (3 years)\n\nPak Pacific Shipping Solutions \n\nEnsure to make the business strategic solutions and meet with the \n\nCustomer and dealing with the shipping lines with based on the client\n\nServices.\n\nAssist Assistant Manager in all operational aspects.\n\nContribution to the team performance,development and effective working\n\nrelationship with the Management.\n\nReporting Daily/Weekly/Monthly Analysis to the higher authorities  and\n\nthe Shipping Lines as per provided format in the excel sheet.\n\nOutput to be monitored against target on volumes & accuracy as per \n\nmaster record within the deadlines..\n\n\n\n\n\nEducation\n\nBS in Computer Science\n\nDadabhoy Institute Of Higher Education\n\n2015\n\n\n\n3.0 CPGA\n\n\n\n\n\n\n\n\n\n\n\n\n\nLanguages\n\n\n\n\n\n     English, Urdu and Pashto\n\n\n\n\n\n\n\n\n\n\n\n\n\nPersonal Information\n\n\n\n\n\n  Father Name:			           Shamsuddin\n\n Date of Birth:                                        18-03-1988\n\n Nationality:			                       Pakistan\n\n  Religion:			                          Islam\n\n Gender:				               Male\n\n Marital Status:			              Single\n\n  NIC #                                                  42501-9140832-7\n\n\n\n\n\n\n\nReference\n\n\n\n\n\n	        Will be furnish upon request.', 'BS  Computer Science ', '3 years', 'Java,C#,ASP.NET,Management,'),
(63, 61, '2019-08-19', 'Male', 'Married', 'Pakistan', 'Karachi', '0322-1257134', 'CURRICULUM VITAE\n\nMUHAMMAD ALI ASKARI\n\nHouse No. R- 815 Sector-8 North Karachi.\n\nCell No. 0341-2855098.\n\nEmail:-aliask2000@yahoo.com\n\n______________________________________________________________________________\n\n\n\nOBJECTIVE:\n\n\n\nTo seek a professional challenging position which allow to apply my skill and experience and also provide me opportunity for career growth and personal development.\n\n\n\nPERSONAL  INFORMATION:\n\n\n\nFather’s Name				:	Jalal Haider Askari\n\n\n\nReligion					:	Islam\n\n\n\nN.I.C No					:	42101-1739339-5\n\n\n\nNationality					:	Pakistani\n\n\n\nDomicile					:	Karachi (Sindh)\n\n\n\nMarital Status				:	Single\n\n\n\nACADEMIC QUALIFICATION:\n\n\n\nMS in Computer Science			:	University of Karachi.\n\n\n\nSKILLS:\n\n\n\nC#, ASP.NET, Ms.Office Word, Excel, PowerPoint, MS.Windows, Internet \n\n		\n\nJOB  EXPERIENCE:\n\n	\n\n2 Years worked in National Bank of Pakistan, as an IT Office Assistant.', 'MS  Computer Science ', '2 Years', 'C#,ASP.NET,'),
(64, 62, '2019-08-19', 'Male', 'Unmarried', 'Pakistan', 'Karachi', '0322-1257134', 'CURRICULUM VITAE \n\n                                                                         ALI RAZA \n\nAddress: Plot # A-58/10,Flat # 12, 3rd floor , Al-Umair Building Street # 3, Dehli Colony, Karachi.\n\nCell#03422411170\n\nCARRER OBJECT:\n\nSeeking a challenging employment opportunity that effectively utilize my skills and expertise in the organization that would give me scope to apply my knowledge and skills in tune with latest trends and be a part of team that dynamically works towards the destination of the organization. \n\nACADEMIC QUALIFICATION:\n\nBS Computer Science Graduation from Karachi University 2014.\n\nIntermediate in Pre-Engineering from Nabi Bagh Z.M. Govt. Science College 2011.\n\nMatriculation in Science from Qamar ul Islam Govt. Boys Secondary School 2009.\n\n\n\nPERSONAL INFORMATION\n\nFather’s Name               : Abdul Wahid \n\nNationality                      : Pakistani\n\nReligion                            : Islam\n\nLanguages                        : Urdu, English & Punjabi\n\n	Marital  Status                 : Single\n\nDate of Birth                   : 16th jan 1994\n\nCNIC #                               : 42301-2230267-7\n\n\n\n\n\nEXPERIENCE:\n\n8 years experience working as a Software Engineer at Interactive Media since 2013.\n\n\n\nCOMPUTER SKILLS:\n\nMS Office, HTML, CSS, JavaScript, C#, ASP.NET, PHP Development, Adobe Photoshop\n\nREFERENCE: \n\nWill be furnished upon request.', 'BS  Computer Science ', '8 years', 'HTML,CSS,Java,C#,ASP.NET,PHP,'),
(65, 63, '2019-08-19', 'Male', 'Unmarried', 'Pakistan', 'Karachi', '0322-1257134', 'Talal Ahmed\n\n\n\ntahmed530@gmail.com\n\n (+92) 322-1257134\n\n5/94, Hashim Raza Road, Model Colony, Karachi, Pakistan\n\nhttps://talalonline.000webhostapp.com/\n\n\n\n\n\nTalal Ahmed\n\n\n\ntahmed530@gmail.com\n\n (+92) 322-1257134\n\n5/94, Hashim Raza Road, Model Colony, Karachi, Pakistan\n\nhttps://talalonline.000webhostapp.com/\n\n\n\n\n\n\n\n		\n\n\n\n\n\n	Objective\n\nHighly ambitious, hardworking and achievement oriented individual driven by goals and challenges. An enthusiastic graduate looking for the right choice that can provide the best opportunity to grow my abilities so that I can serve on a responsible position.\n\nProfessional Experience\n\n2018 - 2019\n\n\n\nInteractive Media\n\nWeb Applications Developer (PHP, MySQL)\n\nWorked on and maintained 25 projects in the span of 0.5 year\n\nProjects ranging from Business Websites to E-commerce Web Applications\n\nManaged Front-end Web Development Team in most projects \n\nWorked on projects with very tight deadlines of 2-3 days\n\nSuccessfully completed and submitted all projects\n\n\n\nEducation\n\n\n\n\n\n\n\n2019\n\n\n\nMS Computer Gamer\n\nPresidential Initiative for Artificial Intelligence and Computing (PIAIC)\n\n\n\n2019\n\n\n\nPS – Computer Science\n\nPAF-KIET, Karachi\n\n\n\n2013\n\n\n\nIntermediate (Pre-Engineering)\n\nPECHS Education Foundation College, Karachi\n\n\n\n2011\n\n\n\nMatriculation (Science)\n\nFazaia Inter College Malir Cantt, Karachi\n\n \n\n\n\nComputing Skills\n\nProg. Languages\n\n-\n\nPython, C#, PHP, Assembly\n\nWeb Development\n\n-\n\nPython (Flask, Django), PHP, ASP.NET, Bootstrap, HTML, CSS, JavaScript, jQuery, AJAX\n\nDatabases\n\n-\n\nMySQL, Microsoft SQL Server, Microsoft Access\n\nOperating Systems\n\n-\n\nWindows, Linux (Ubuntu, Arch Linux, Linux Mint, Debian)\n\n\n\nFYP\n\n\n\n\n\nCV- Ranker\n\nDescription:\n\nAn online Job Portal where users can search jobs related to their Education, Professional Experience and Skills. The Job Applicants can upload their CVs in DOC/PDF file formats. Our algorithms extract out Education, Experience and Skills from the CV and match these with the Education, Experience and Skills listed on the Job post. The CV is then ranked by our algorithms on the basis of the matched data of the CV and Job post. The best matched CV is ranked the highest. This ranking helps Job Posters to find the perfect candidate for their jobs and makes hiring procedure hassle-free.\n\nTools Used for Data Extraction and CV Ranking:\n\nNatural Language Processing, Self-made Matching and Ranking Algorithms\n\nLanguages & Framework:\n\nPython 3, Flask, Bootstrap, Html5, CSS, JavaScript, jQuery, AJAX\n\n\n\nCourse Projects\n\n\n\nProject Name\n\nProgramming Language & DB\n\nCourse Name\n\nE-Commerce Website\n\nPHP, MySQL\n\nDatabase Management Systems\n\nStudent Learning Management System\n\nC#, Microsoft Access\n\nObject  Oriented  Analysis & Design\n\nElectronic Store\n\nC#, Microsoft Access\n\nDesign Patterns\n\nNumber System Converter (Binary, Decimal, Octal, Hexadecimal Conversions)\n\nAssembly Language\n\nComputer Organization & Assembly Language\n\nFile Transfer Protocol Server\n\nC#, Microsoft SQL Server\n\nData Communications & Networking\n\nLinux from Scratch\n\nUNIX, Linux Kernel & Arch Linux Shell\n\nOperating Systems\n\n\n\n\n\n \n\nPortfolio\n\nhttps://talalonline.000webhostapp.com/', 'MS Computer Science', '5 year', 'PHP,MySQL,Python,C#,ASP.NET,Bootstrap,HTML,CSS,Java,AJAX,Html,Management,Networking,');

-- --------------------------------------------------------

--
-- Table structure for table `skills`
--

CREATE TABLE `skills` (
  `skill_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `skill` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `skills`
--

INSERT INTO `skills` (`skill_id`, `user_id`, `skill`) VALUES
(1, 1, 'Java, C#, Python'),
(2, 2, 'Android'),
(3, 3, 'Web Engineering, Web Development'),
(4, 4, 'Business Administration'),
(5, 5, 'Accounting, Finance');

-- --------------------------------------------------------

--
-- Table structure for table `skill_data`
--

CREATE TABLE `skill_data` (
  `id` int(11) NOT NULL,
  `label` varchar(100) NOT NULL,
  `data` longtext NOT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `skill_data`
--

INSERT INTO `skill_data` (`id`, `label`, `data`, `score`) VALUES
(1, 'C#', 'c#,C#,csharp,c sharp,c-sharp', 20),
(2, 'python', 'python,Python', 20),
(3, 'Java', 'Java,java', 20),
(4, 'PHP', 'PHP,P.H.P,Php,p-h-p,P H P', 20),
(5, 'Dot net', 'Dot net,.Net,dot net,dot-net,Dot.Net,Dot_net,Dot-net', 20),
(6, 'Mysql', 'Mysql,MYSQL,MYsql,mysql,MySQL', 20),
(7, 'Android', 'Android,android,Mobile applications,Mobile app', 20),
(8, 'Bootstrap', 'Bootstrap,bootstrap,Boot-strap', 20),
(9, 'HTML', 'HTML,html,H.T.M.L', 20),
(10, 'Graphic designing', 'Graphic designing,graphic designing,Graphic designer,Graphic-designing,Graphic-designer', 20),
(11, 'CSS', 'CSS,C.S.S', 20),
(12, 'XML', 'XML,xml,X.M.L,Xml', 20),
(13, 'MS word', 'MS word,MS-Word,MS.Word,MS Word,Ms word,ms word', 20),
(14, 'MS-Office', 'MS-Office,MS Office,MS.Office,ms office,MS_Office', 20),
(15, 'MS-Excel', 'MS-Excel,MS_Excel,MS.Excel,MS excel,ms excel', 20),
(16, 'Programming', 'Programming,Programmer,coding skills,Coder,coding', 20),
(17, 'Matlab', 'MATLAB,Matlab,MAT-LAB,matlab,MATlab', 20),
(18, 'Micro controller', 'Micro Controller,Micro-Controller,Micro_Controller', 20),
(19, 'JavaScript', 'JavaScript,Javascript,Java-Script,Java_Script,javascript,Java Script', 20),
(20, 'MVC', 'MVC,M.V.C,M V C,Model view controller,model view controller,mvc', 20),
(21, 'AJAX', 'AJAX,Ajax,ajax', 20),
(22, 'C++', 'c++,C++,cpp,CPP', 20),
(23, 'ASP.NET', 'ASP.NET,asp,aspnet,asp.net,asp dot net,ASP', 20),
(24, 'English', 'English speaking,English writing', 20),
(25, 'analytics', 'analytics,Analytics,ANALYTICS', 20),
(26, 'numeracy', 'numeracy,Numeracy,NUMERACY', 20),
(27, 'accounting', 'accounting,Accounting,ACCOUNTING', 20);

-- --------------------------------------------------------

--
-- Table structure for table `universities`
--

CREATE TABLE `universities` (
  `uni_id` int(50) NOT NULL,
  `uni_name` varchar(50) NOT NULL,
  `uni_rank` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `universities`
--

INSERT INTO `universities` (`uni_id`, `uni_name`, `uni_rank`) VALUES
(1, 'Stanford', 100),
(2, 'PAF-KIET', 20),
(3, 'NYU', 70),
(4, 'Cornell', 90),
(5, 'Indus', 5);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(50) NOT NULL,
  `firstname` varchar(50) NOT NULL,
  `lastname` varchar(50) NOT NULL,
  `emailid` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `registerdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `firstname`, `lastname`, `emailid`, `password`, `registerdate`) VALUES
(60, 'Talal', 'Ahmed', 'tahmed530@gmail.com', '$5$rounds=535000$2/Um8wfktg8xQz5R$ILyrDafww1zRpZRZk65Pibc7TntdtDrOxxuTzQaLd09', '2019-08-19 07:08:45'),
(61, 'Abdullah', 'Riaz', 'ar@gmail.com', '$5$rounds=535000$Gv3JcQKUjMqzYlqM$QQKDyolbtCT.aUWNkwhX/XnTFNGbfWS1UKQAS3ZR8L8', '2019-08-19 08:15:03'),
(62, 'Usman', 'Ahmed', 'usmanahmed@gmail.com', '$5$rounds=535000$peveO0aDf7XHSFvW$M8IS4OZkAvhdano2rFcbZh25gMM2fjWMmE9tOVS/g5.', '2019-08-19 08:27:50'),
(63, 'Waqar', 'Ahmed', 'waqarpaf@gmail.com', '$5$rounds=535000$eyKtu3bsLZgpeN.H$CytjjlojvY2xRcWG0QPcZgPQ.5p.1fmjuWvM8onuPK2', '2019-08-19 08:29:59');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `applied_jobs`
--
ALTER TABLE `applied_jobs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `education`
--
ALTER TABLE `education`
  ADD PRIMARY KEY (`edu_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `edu_data`
--
ALTER TABLE `edu_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `experience`
--
ALTER TABLE `experience`
  ADD PRIMARY KEY (`exp_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `exp_data`
--
ALTER TABLE `exp_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `extract_cv`
--
ALTER TABLE `extract_cv`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `job_posts`
--
ALTER TABLE `job_posts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `organization`
--
ALTER TABLE `organization`
  ADD PRIMARY KEY (`org_id`);

--
-- Indexes for table `personal_info`
--
ALTER TABLE `personal_info`
  ADD PRIMARY KEY (`Serial_No`);

--
-- Indexes for table `posted_jobs`
--
ALTER TABLE `posted_jobs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `profile`
--
ALTER TABLE `profile`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `skills`
--
ALTER TABLE `skills`
  ADD PRIMARY KEY (`skill_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `skill_data`
--
ALTER TABLE `skill_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `universities`
--
ALTER TABLE `universities`
  ADD PRIMARY KEY (`uni_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `applied_jobs`
--
ALTER TABLE `applied_jobs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=141;
--
-- AUTO_INCREMENT for table `education`
--
ALTER TABLE `education`
  MODIFY `edu_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `edu_data`
--
ALTER TABLE `edu_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;
--
-- AUTO_INCREMENT for table `experience`
--
ALTER TABLE `experience`
  MODIFY `exp_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `exp_data`
--
ALTER TABLE `exp_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `extract_cv`
--
ALTER TABLE `extract_cv`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `job_posts`
--
ALTER TABLE `job_posts`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;
--
-- AUTO_INCREMENT for table `organization`
--
ALTER TABLE `organization`
  MODIFY `org_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `personal_info`
--
ALTER TABLE `personal_info`
  MODIFY `Serial_No` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `posted_jobs`
--
ALTER TABLE `posted_jobs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=430;
--
-- AUTO_INCREMENT for table `profile`
--
ALTER TABLE `profile`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;
--
-- AUTO_INCREMENT for table `skills`
--
ALTER TABLE `skills`
  MODIFY `skill_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `skill_data`
--
ALTER TABLE `skill_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
--
-- AUTO_INCREMENT for table `universities`
--
ALTER TABLE `universities`
  MODIFY `uni_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
