variable "core_instance_type" {
    default = "m5.xlarge"
    type = string
    description = "specify the core instance type you wish to spin up"
}

variable "master_instance_type" {
    default = "m5.xlarge"
    type = string
    description = "specify the master instance type you wish to spin up"
}

variable "core_instance_count" {
    default = 2
    type = number
    description = "number of core instance you want in the cluster"
}

variable "bootstrap_action_path" {
    default = "s3://mybucket/myfilefolder/jarfiles"
    type = string
    description = "specify the path where your initialization scripts/files are located"
}

variable "master_instance_group_ebs_size" {
  type        = number
  description = "Master instances volume size, in gibibytes (GiB)"
}

variable "master_instance_group_ebs_type" {
  type        = string
  description = "Master instances volume type. Valid options are `gp2`, `io1`, `standard` and `st1`"
}

variable "master_instance_group_ebs_volumes_per_instance" {
  type        = number
  description = "The number of EBS volumes with this configuration to attach to each EC2 instance in the Master instance group"
}


variable "core_instance_group_ebs_size" {
  type        = number
  description = "Core instances volume size, in gibibytes (GiB)"
}

variable "core_instance_group_ebs_type" {
  type        = string
  description = "Core instances volume type. Valid options are `gp2`, `io1`, `standard` and `st1`"
}

variable "core_instance_group_ebs_volumes_per_instance" {
  type        = number
  description = "The number of EBS volumes with this configuration to attach to each EC2 instance in the Core instance group"
}

variable "core_instance_group_autoscaling_policy" {
  type        = string
  description = "String containing the EMR Auto Scaling Policy JSON for the Core instance group"
  default     = "core_instance_group-autoscaling_policy.json.tpl"
}

#-----------------Task Instance Group----------------#

variable "task_instance_group_name" {
  type        = string
  description = "Name of the Master instance group"
  default = "taskGroup"
}


variable "task_instance_group_instance_type" {
  type        = string
  description = "EC2 instance type for all instances in the task instance group"
  default = "m5.xlarge"
}


variable "task_instance_group_instance_count" {
  type        = number
  description = "Target number of instances for the task instance group. Must be at least 1"
  default     = 1
}


variable "task_instance_group_ebs_size" {
  type        = number
  description = "task instances volume size, in gibibytes (GiB)"
  default = 30
}


variable "task_instance_group_ebs_type" {
  type        = string
  description = "task instances volume type. Valid options are `gp2`, `io1`, `standard` and `st1`"
  default     = "gp2"
}

variable "task_instance_group_ebs_iops" {
  type        = number
  description = "The number of I/O operations per second (IOPS) that the task volume supports"
  default     = null
}


variable "task_instance_group_ebs_volumes_per_instance" {
  type        = number
  description = "The number of EBS volumes with this configuration to attach to each EC2 instance in the task instance group"
  default     = 1
}


variable "task_instance_group_bid_price" {
  type        = string
  description = "Bid price for each EC2 instance in the task instance group, expressed in USD. By setting this attribute, the instance group is being declared as a Spot Instance, and will implicitly create a Spot request. Leave this blank to use On-Demand Instances"
  default     = 0.3
}

variable "task_instance_group_autoscaling_policy" {
  type        = string
  description = "String containing the EMR Auto Scaling Policy JSON for the task instance group"
  default = "task_instance_group-autoscaling_policy.json.tpl"
}

