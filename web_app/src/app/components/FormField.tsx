import React, {  useRef, useState } from 'react';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined'; 
import CloseIcon from '@mui/icons-material/Close';
import { Box,  IconButton, Typography,  Grid, Tooltip } from '@mui/material';

interface FormFieldProps {
    readonly id: string;
    readonly labelText: string;
    readonly placeholder?: string;
    readonly helperText?: string;
    readonly tooltipTitle: string,
    readonly tooltipContent: React.ReactNode;
    readonly children: React.ReactNode;
    readonly error: boolean;
    readonly errorText: string;
};

export function FormField({
    id,
    labelText,
    placeholder,
    helperText,
    tooltipTitle,
    tooltipContent,
    children,
    error,
errorText,}: FormFieldProps) {

const styles = {    
    iconButton: {
        '&:hover': {
            backgroundColor: 'transparent',
        },
    },
    popoverContent: {
        padding: '1px',
        maxWidth: '600px',
        marginTop:'-10px',
    },
};
        const inputRef = useRef<HTMLElement>(null);

        const [openTooltip, setOpenTooltip] = useState(false);

        const handleTooltipOpen = () => {
            setOpenTooltip(true);
        };

        const handleTooltipClose = () => {
            setOpenTooltip(false);
        };

        return (
            <Box sx={{ display: 'block', alignItems: 'left', flexDirection: 'column', gap: 1, ml: '5px', width: 'auto' }}>
                <Box sx={{ display: 'flex', alignItems: 'left', width: 'auto' }}>
                    <IconButton
                        size="small"
                        onClick={handleTooltipOpen}>
                        <InfoOutlinedIcon fontSize="small" /></IconButton>
                    <Typography variant='subtitle1' component="label" htmlFor={id + '-field'} sx={{ color: '#313132', fontSize:'16px', fontWeight:'700', }}>
                        {labelText}
                    </Typography>
                </Box>
                <Box ref={inputRef} sx={{ display: 'inline-flex', alignItems: 'center', width: 'auto' }}>
                    <Tooltip arrow placement="right"
                        title={
                            <Box>
                                <Grid container spacing={2} >
                                    <Grid item xs={8} sx={{ padding: "1px" }}>
                                        <Typography sx={{ fontWeight: 600 }}>{tooltipTitle}</Typography>
                                    </Grid>
                                    <Grid item xs={4} sx={{ padding: "1px" }}>
                                        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                                            <IconButton aria-label="close"
                                                onClick={handleTooltipClose}
                                                size="small">
                                                <CloseIcon fontSize="small" />
                                            </IconButton>
                                        </Box>
                                    </Grid>
                                </Grid>
                                <Typography sx={styles.popoverContent}>{tooltipContent}</Typography>
                            </Box>
                        }
                        open={openTooltip}
                        onClose={handleTooltipClose}
                        disableHoverListener
                        disableFocusListener
                        disableTouchListener
                        PopperProps={{
                            anchorEl: inputRef.current,
                        }}
                    >
                        <Box sx={{ display: 'table-cell', paddingLeft:'5px' }}>
                            {children}
                        </Box>
                    </Tooltip>
                </Box>
                {error &&
                    <Typography variant="caption" sx={{ mb: 1, color: 'rgba(0,0,0,0.6)', display: 'block' }}>
                        {error ? errorText : ""}
                    </Typography>
                }
                <Typography variant="caption" sx={{ mb: 1, color: '#767676', display: 'block', fontSize: '16px', mt: 0, paddingLeft: '10px', fontFamily: "'BC Sans', 'Noto Sans',  Arial, sans-serif" }}>
                    {helperText}
                </Typography>
            </Box>
        );
    }
    
